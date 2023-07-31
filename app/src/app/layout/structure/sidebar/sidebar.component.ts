/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { UntypedFormControl } from '@angular/forms';

import { ReplaySubject, Subscription } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { CmdbCategoryTree } from '../../../framework/models/cmdb-category';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';

import { SidebarService } from '../../services/sidebar.service';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { CollectionParameters } from '../../../services/models/api-parameter';

import {AccessControlPermission} from "../../../acl/acl.types";

@Component({
  selector: 'cmdb-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit, OnDestroy {

  /**
   * Global un-subscriber for http calls to the rest backend.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Category data
   */
  public categoryTree: CmdbCategoryTree;
  private categoryTreeSubscription: Subscription;

  /**
   * Types params
   */
  public typesParams: CollectionParameters = {
    filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
  };

  /**
   * Type data
   */
  public typeList: CmdbType[] = [];
  public unCategorizedTypes: CmdbType[] = [];
  private unCategorizedTypesSubscription: Subscription;

  /**
   * Filter
   */
  public filterTerm: UntypedFormControl = new UntypedFormControl('');
  private filterTermSubscription: Subscription;

  /**
   * String representation of currently selected tab menu in sidebar (Default is Categories)
   */
  selectedMenu: string = 'categories';

  constructor(private sidebarService: SidebarService, private typeService: TypeService, private renderer: Renderer2) {
    this.categoryTreeSubscription = new Subscription();
    this.unCategorizedTypesSubscription = new Subscription();
    this.filterTermSubscription = new Subscription();
  }

  

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'sidebar-fixed');
    this.sidebarService.loadCategoryTree();
    this.categoryTreeSubscription = this.sidebarService.categoryTree.asObservable().subscribe((categoryTree: CmdbCategoryTree) => {
      this.categoryTree = categoryTree;
      this.unCategorizedTypesSubscription = this.typeService.getUncategorizedTypes(AccessControlPermission.READ,
        false).subscribe(
          (apiResponse: APIGetMultiResponse<CmdbType>) => {
            this.unCategorizedTypes = apiResponse.results as Array<CmdbType>;
          });

      this.typeService.getTypes(this.typesParams).pipe(takeUntil(this.subscriber)).subscribe(
        (apiResponse: APIGetMultiResponse<CmdbType>) => {
          this.typeList = apiResponse.results as Array<CmdbType>;
        });
    });
  }

  public ngOnDestroy(): void {
    this.categoryTreeSubscription.unsubscribe();
    this.unCategorizedTypesSubscription.unsubscribe();
    this.filterTermSubscription.unsubscribe();
    this.renderer.removeClass(document.body, 'sidebar-fixed');
  }

  
  /**
   * Toggles the activated menu tabs (categories and locations)
   * 
   * @param selection :string = String representation of the selected menu
   */
  onSidebarMenuClicked(selection: HTMLDivElement){
    this.selectedMenu = selection.getAttribute('value');
  }

}
