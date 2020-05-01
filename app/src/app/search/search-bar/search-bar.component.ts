/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
import { Subscription } from 'rxjs';
import { SearchBarTagComponent } from './search-bar-tag/search-bar-tag.component';
import { ActivatedRoute, NavigationEnd, Route, Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { debounceTime } from 'rxjs/operators';
import { CategoryService } from '../../framework/services/category.service';
import { CmdbCategory } from '../../framework/models/cmdb-category';
import { SearchService } from '../search.service';
import { ObjectService } from '../../framework/services/object.service';

import * as $ from 'jquery';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit, OnDestroy {

  // Child components
  @ViewChild('tagInput', { static: false }) tagInput: ElementRef;
  @ViewChild('inputDropdown', { static: false }) inputDropdown: ElementRef;
  @ViewChild('inputSubDropdown', { static: false }) inputSubDropdown: ElementRef;
  @ViewChildren(SearchBarTagComponent) searchBarTagComponents: QueryList<SearchBarTagComponent>;

  // Tabs
  private currentFocus: number = 0;
  private maxTabLength: number = 5;

  // Tags data
  public tags: SearchBarTag[] = [];

  // Form
  public searchBarForm: FormGroup;

  // Dropdown
  public possibleTextResults: number = 0;
  public isExistingPublicID: boolean = false;
  public possibleTypes: CmdbType[] = [];
  public possibleCategories: CmdbCategory[] = [];

  // Subscriptions
  private routeChangeSubscription: Subscription;
  private textRegexSubscription: Subscription;
  private isExistingPublicIDSubscription: Subscription;
  private typeRegexSubscription: Subscription;
  private inputControlSubscription: Subscription;

  constructor(private router: Router, private route: ActivatedRoute, private searchService: SearchService,
              private typeService: TypeService, private categoryService: CategoryService, private objectService: ObjectService) {

    this.searchBarForm = new FormGroup({
      inputControl: new FormControl('')
    });
    this.textRegexSubscription = new Subscription();
    this.isExistingPublicIDSubscription = new Subscription();
    this.typeRegexSubscription = new Subscription();
    this.inputControlSubscription = new Subscription();
    this.routeChangeSubscription = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const searchQuery = this.route.snapshot.queryParams.query;
        if (searchQuery !== undefined) {
          this.tags = JSON.parse(searchQuery) as SearchBarTag[];
        } else {
          this.tags = [];
        }
      }
    });
  }

  public ngOnInit(): void {

    this.inputControl.valueChanges.pipe(debounceTime(300)).subscribe((changes: string) => {
      if (changes.trim() !== '') {
        this.textRegexSubscription = this.searchService.getEstimateValueResults(changes).subscribe((counter: number) => {
          this.possibleTextResults = counter;
        });
        if (!isNaN(+changes)) {
          this.isExistingPublicIDSubscription = this.objectService.getObject(+changes).subscribe(() => {
              this.isExistingPublicID = true;
            },
            (error) => {
              this.isExistingPublicID = false;
            });
        }
        this.typeRegexSubscription = this.typeService.getTypesBy(changes).subscribe((typeList: CmdbType[]) => {
          this.possibleTypes = typeList;
        });
        this.typeRegexSubscription = this.categoryService.getCategoriesBy(changes).subscribe((categoryList: CmdbCategory[]) => {
          this.possibleCategories = categoryList;
        });
      } else {
        this.possibleTextResults = 0;
        this.possibleTypes = [];
        this.possibleCategories = [];
      }

    });
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
        tag.searchText = ValidatorService.validateRegex(searchTerm);
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
      case 'publicID':
        tag.settings = { publicID: searchTerm } as SearchBarTagSettings;
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
    $('[tabindex=' + (currentIDx) + ']').find('[data-toggle="collapse"]').first().click();
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
      $('[tabindex=' + this.currentFocus + ']').focus();
    }, 0);
  }

  public ngOnDestroy(): void {
    // ToDo: provisionally commented out. To be used later.
    // this.routeChangeSubscription.unsubscribe();
    this.textRegexSubscription.unsubscribe();
    this.typeRegexSubscription.unsubscribe();
    this.inputControlSubscription.unsubscribe();
  }

}
