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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { ReplaySubject } from 'rxjs';

import { ConfigEditBaseComponent } from '../config.edit';

import { RenderResult } from '../../../../models/cmdb-render';
import { CmdbType } from '../../../../models/cmdb-type';

import { CollectionParameters } from '../../../../../services/models/api-parameter';

import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { nameConvention } from '../../../../../layout/directives/name.directive';

@Component({
  selector: 'cmdb-location-field-edit',
  templateUrl: './location-field-edit.component.html',
  styleUrls: ['./location-field-edit.component.scss'],
})
export class LocationFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  constructor(private cd: ChangeDetectorRef) {
    super();
  }

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Name form control.
   */
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Label form control.
   */
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Type form control.
   */
  public typeControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);

  /**
   * Summary form control.
   */
  public summaryControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);

  /**
   * Type list for reference selection
   */
  public typeList: CmdbType[] = [];
  public filteredTypeList: CmdbType[] = [];
  public totalTypes: number = 1;

  /**
   * Type loading indicator.
   */
  public typeLoading: boolean = false;

  /**
   * Begin with first page.
   */
  public readonly initPage: number = 1;
  public page: number = this.initPage;

  /**
   * Filter query from the table search input.
   */
  public filter: string;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Nested summaries
   */
  public summaries: any[] = [];

  /**
   * Object list for default reference value
   */
  public objectList: RenderResult[];

  /**
   * Types params
   */
  public typesParams: CollectionParameters = {
    filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
  };

  /**
   * Reference form control.
   */
  public referenceGroup: UntypedFormGroup = new UntypedFormGroup({ type_id: this.typeControl });

  /** LIFE CYCLE - SECTION **/
  public ngOnInit(): void {
    this.setDraggable("false");
    
    this.form.addControl('name', this.nameControl);
    this.form.addControl('label', this.labelControl);
    this.form.addControl('ref_types', this.typeControl);
    this.form.addControl('summaries', this.summaryControl);

    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);

    this.typeList = [this.getRootElement() as CmdbType];
    this.prepareSummaries();
    this.cd.markForCheck();
  }

  public onChange() {
    const { ref_types } = this.data;
    if (Array.isArray(this.data.ref_types) && ref_types && ref_types.length === 0) {
      this.objectList = [];
      this.filteredTypeList = [];
      this.data.value = '';
    } else {
      this.objectList = this.getRootElementRenderResult();
      this.prepareSummaries();
    }
  }

  /**
   * Destroy subscriptions after closed.
   */
  public ngOnDestroy(): void {
    this.setDraggable("true");
    this.subscriber.next();
    this.subscriber.complete();
  }

  /** HELPER - SECTION **/

    /**
   * Structure of the Summaries depending on the selected types
   * @private
   */
    private prepareSummaries() {
      if (this.data.ref_types) {
        if (!Array.isArray(this.data.ref_types)) {
          this.data.ref_types = [this.data.ref_types];
        }
        this.filteredTypeList = this.typeList.filter(type => this.data.ref_types.includes(type.public_id));
        this.summaries = this.data.summaries ? this.data.summaries : this.summaries;
      }
    }

   /**
   * Name converter on ng model change.
   * @param name
   */
  public onNameChange(name: string){
    this.data.name = nameConvention(name);
  }

  //TODO: this is just a work around and need to be set with proper angular code 
  //sets the special control location to not draggable when there is already a location present
  private setDraggable(isDraggable: string): void{
    let opacity: string = isDraggable == "true" ? "1.0" : "0.5";

    //this only works if the special control "location" is the 2nd element
    let specialControlLocation: Element = document.getElementById('specialControls').getElementsByClassName('list-group-item')[1];
    specialControlLocation.setAttribute('draggable', isDraggable);
    (specialControlLocation as HTMLElement).style.opacity = opacity;
  }

  private getRootElement(){
    return {
      public_id: -1,
          editor_id: 1,
          name: 'root',
          label: 'Root',
          active: true,
          author_id: 1,
          version: "1.0.0",
          creation_time: new Date(),
          last_edit_time: new Date(),
          fields: [
  
          ],
          render_meta: {
              icon: 'fas fa-globe',
              externals: [],
              sections: [],
              summary: {
                  fields:[]
              },
          },
    };
  }

  private getRootElementRenderResult(): [RenderResult]{
    return [{
          current_render_time: {$date: '1'},
          object_information:{
              object_id: -1,
              creation_time: {$date: '1'},
              last_edit_time: {$date: '1'},
              author_id: 1,
              author_name: 'Admin',
              active: true,
              version: '1.0.0'

          },
          type_information:{
              type_id: 1,
              type_label: 'Root',
              type_name: 'root',
              version: '1.0.0',
              creation_time: {$date: '1'},
              author_id: 1,
              author_name: 'Admin',
              active: true,
              acl: {activated: false},
              icon: 'fas fa-globe'

          },
          externals: [],
          fields:[],
          sections: [],
          summaries: [],
          summary_line: "",
      }];
  }
}


