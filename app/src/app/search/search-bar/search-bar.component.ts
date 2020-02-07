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
import { TypeService } from '../../framework/services/type.service';
import { CmdbType } from '../../framework/models/cmdb-type';
import { Subscription } from 'rxjs';
import { SearchBarTagComponent } from './search-bar-tag/search-bar-tag.component';
import { ActivatedRoute, NavigationEnd, Route, Router } from '@angular/router';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit, OnDestroy {

  // Child components
  @ViewChild('tagInput', { static: false }) tagInput: ElementRef;
  @ViewChildren(SearchBarTagComponent) searchBarTagComponents: QueryList<SearchBarTagComponent>;

  // Tags data
  public tags: SearchBarTag[] = [];
  public typeList: CmdbType[] = [];

  // Subscriptions
  private routeChangeSubscription: Subscription;
  private typeListSubscription: Subscription;

  constructor(private router: Router, private route: ActivatedRoute, private typeService: TypeService) {
    this.tags = [];
    this.typeList = [];
    this.typeListSubscription = new Subscription();
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
    this.typeListSubscription = this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
  }

  public addTag(input: string | number, open: boolean = false) {
    if (input !== '') {
      const inputType = (!isNaN(+input) ? 'number' : 'string');
      let searchForm = 'textSearch';
      const settings = {} as SearchBarTagSettings;
      const possibleType = this.typeList.find(x => (x.label === input || x.name === input));
      if (possibleType) {
        searchForm = 'typeID';
        settings.publicID = possibleType.public_id;
      } else if (inputType === 'string') {
        searchForm = 'textSearch';
      } else if (inputType === 'number') {
        searchForm = 'publicID';
      }

      this.tagInput.nativeElement.value = '';
      const index = (this.tags.push({ searchText: input, searchForm, settings } as SearchBarTag) - 1);
      // Try to open dropdown
      if (open) {
        setTimeout(() => {
          const searchTagComponent = this.searchBarTagComponents.toArray()[index];
          searchTagComponent.toggleDropDown();
        }, 120);
      }
    }
  }

  public updateTag(changes: SearchBarTag) {
    const index: number = this.tags.indexOf(changes);
    console.log(changes);
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

  public clearAll() {
    this.tags = [];
  }

  public callSearch() {
    if (this.tags.length > 0) {
      this.router.navigate(['/search'], { queryParams: { query: JSON.stringify(this.tags) } });
    }
  }

  public ngOnDestroy(): void {
    this.routeChangeSubscription.unsubscribe();
    this.typeListSubscription.unsubscribe();
  }

}
