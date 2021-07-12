/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  QueryList,
  ViewChild,
  ViewChildren
} from '@angular/core';
import { SearchBarTag, SearchBarTagSettings } from './search-bar-tag/search-bar-tag';
import { ValidatorService } from '../../services/validator.service';
import { TypeService } from '../../framework/services/type.service';
import { CmdbType } from '../../framework/models/cmdb-type';
import { ReplaySubject } from 'rxjs';
import { SearchBarTagComponent } from './search-bar-tag/search-bar-tag.component';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';
import { CategoryService } from '../../framework/services/category.service';
import { CmdbCategory } from '../../framework/models/cmdb-category';
import { SearchService } from '../search.service';
import { ObjectService } from '../../framework/services/object.service';
import * as $ from 'jquery';
import { NumberSearchResults } from '../models/search-result';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit, OnDestroy {

  // Child components
  @ViewChild('tagInput') tagInput: ElementRef;
  @ViewChild('inputDropdown') inputDropdown: ElementRef;
  @ViewChild('inputSubDropdown') inputSubDropdown: ElementRef;
  @ViewChildren(SearchBarTagComponent) searchBarTagComponents: QueryList<SearchBarTagComponent>;

  // Tabs
  private currentFocus: number = 0;
  private maxTabLength: number = 5;

  // Tags data
  public tags: SearchBarTag[] = [];

  // Form
  public searchBarForm: FormGroup;

  // Dropdown
  public possibleTextResults: NumberSearchResults = new NumberSearchResults();
  public possibleRegexResults: NumberSearchResults = new NumberSearchResults();
  public possibleTypes: CmdbType[] = [];
  public possibleCategories: CmdbCategory[] = [];

  // Subscriptions
  private subscriber = new ReplaySubject<void>();

  constructor(private router: Router, private route: ActivatedRoute, private searchService: SearchService,
              private typeService: TypeService, private categoryService: CategoryService) {
    this.searchBarForm = new FormGroup({
      inputControl: new FormControl('')
    });
  }

  public ngOnInit(): void {
    this.syncQuerySearchParameters();
    this.inputControl.valueChanges.pipe(debounceTime(500), distinctUntilChanged()).subscribe((changes: string) => {
      if (changes.trim() !== '') {
        if (ValidatorService.getRegex().test(changes)) {
          this.searchService.getEstimateValueResults(changes).pipe(takeUntil(this.subscriber))
            .subscribe((counter: NumberSearchResults) => {
              this.possibleRegexResults = counter;
            });
        }
        this.searchService.getEstimateValueResults(ValidatorService.replaceTextWithRegex(changes))
          .pipe(takeUntil(this.subscriber))
          .subscribe((counter: NumberSearchResults) => {
            this.possibleTextResults = counter;
          });
        this.typeService.getTypesByNameOrLabel(changes).pipe(takeUntil(this.subscriber))
          .subscribe((typeList: CmdbType[]) => {
            this.possibleTypes = typeList;
          });
        this.categoryService.getCategoriesByName(changes).pipe(takeUntil(this.subscriber))
          .subscribe((categoryList: CmdbCategory[]) => {
            this.possibleCategories = categoryList;
          });
      } else {
        this.possibleTextResults = new NumberSearchResults();
        this.possibleRegexResults = new NumberSearchResults();
        this.possibleTypes = [];
        this.possibleCategories = [];
      }

    });
  }

  /**
   * Parse URL string parameters back to the search bar.
   * @private
   */
  private syncQuerySearchParameters(): void {
    const searchQuery = this.route.snapshot.queryParams.query;
    if (searchQuery !== undefined) {
      this.tags = JSON.parse(searchQuery).filter(tag => tag.searchForm !== 'disjunction') as SearchBarTag[];
    } else {
      this.tags = [];
    }
  }

  public get inputControl(): FormControl {
    return this.searchBarForm.get('inputControl') as FormControl;
  }

  public addTag(searchForm: string, params?: any) {
    const searchTerm = this.inputControl.value;
    const tag = new SearchBarTag(searchTerm, searchForm);
    tag.searchLabel = searchTerm;
    switch (searchForm) {
      case 'text':
        tag.searchText = searchTerm.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&');
        if (!isNaN(parseInt(searchTerm, 10))) {
          tag.settings =  { publicID: searchTerm }  as SearchBarTagSettings;
        }
        break;
      case 'regex':
        tag.searchText = ValidatorService.validateRegex(searchTerm).trim();
        break;
      case 'type':
        const typeIDs: number[] = [];
        for (const type of params) {
          typeIDs.push(type.public_id);
        }
        tag.searchLabel = params.length === 1 ? params[0].label : searchTerm;
        tag.settings = { types: typeIDs } as SearchBarTagSettings;
        break;
      case 'category':
        const categoryIDs: number[] = [];
        for (const category of params) {
          categoryIDs.push(category.public_id);
        }
        tag.searchLabel = params.length === 1 ? params[0].label : searchTerm;
        tag.settings = { categories: categoryIDs } as SearchBarTagSettings;
        break;
      default:
        break;
    }
    this.tags.push(tag);
    this.inputControl.setValue('', { onlySelf: true });
    this.setFocusOnElement(1);
  }

  public updateTag(changes: SearchBarTag) {
    const index: number = this.tags.indexOf(changes);
    if (index !== -1) {
      // If searchText was cleared
      if (changes.searchText === '' || changes.searchText === undefined) {
        this.removeTag(changes);
      } else {
        this.tags[index] = changes;
      }
    }
  }

  public removeTag(tag: SearchBarTag) {
    const index: number = this.tags.indexOf(tag);
    if (index !== -1) {
      this.tags.splice(index, 1);
    }
  }

  public removeLastTag() {
    if (this.inputControl.value.trim() === '') {
      const index: number = this.tags.length - 1;
      if (index !== -1) {
        this.tags.splice(index, 1);
      }
    }
  }

  public clearAll() {
    this.tags = [];
  }

  public callSearch() {
    if (this.inputControl.value.trim() !== '') {
      this.addTag('text');
    }
    if (this.tags.length > 0) {
      this.inputControl.setValue('', { onlySelf: true });
      this.router.navigate(['/search'], { queryParams: { query: JSON.stringify(this.tags) } });
    }
  }

  public openDropdown(currentIDx: number) {
    $('[tabindex=' + (currentIDx) + ']').find('[data-toggle="collapse"]').first().trigger('click');
  }


  public arrowUp(currentIDx?: number) {
    const nextElement = $('[tabindex=' + (currentIDx - 1) + ']');
    if (nextElement.length > 0) {
      this.setFocusOnElement(+nextElement.attr('tabindex'));
    } else {
      for (let i = (currentIDx - 1); i >= 0; i--) {
        const subElement = $('[tabindex=' + (i - 1) + ']');
        if (subElement.length > 0) {
          this.setFocusOnElement(+subElement.attr('tabindex'));
          break;
        }
      }
    }
  }

  public arrowDown(currentIDx?: number) {
    const nextElement = $('[tabindex=' + (currentIDx + 1) + ']');
    if (nextElement.length > 0) {
      this.setFocusOnElement(+nextElement.attr('tabindex'));
    } else {
      for (let i = (currentIDx + 1); i <= this.maxTabLength; i++) {
        const subElement = $('[tabindex=' + (i + 1) + ']');
        if (subElement.length > 0) {
          this.setFocusOnElement(+subElement.attr('tabindex'));
          break;
        }
      }
    }
  }

  public setFocusOnElement(tabIdx?) {
    if (tabIdx) {
      this.currentFocus = tabIdx;
    }
    setTimeout(() => { // this will make the execution after the above boolean has changed
      $('[tabindex=' + this.currentFocus + ']').trigger('focus');
    }, 0);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
