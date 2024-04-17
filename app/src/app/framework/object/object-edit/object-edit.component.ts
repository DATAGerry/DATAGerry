/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { AfterViewInit, Component, HostListener, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

import { ObjectService } from '../../services/object.service';
import { ToastService } from '../../../layout/toast/toast.service';
import { TypeService } from '../../services/type.service';
import { SidebarService } from 'src/app/layout/services/sidebar.service';
import { LocationService } from '../../services/location.service';


import { CmdbMode } from '../../modes.enum';
import { CmdbObject } from '../../models/cmdb-object';
import { RenderResult } from '../../models/cmdb-render';
import { CmdbType } from '../../models/cmdb-type';
import { APIUpdateMultiResponse } from '../../../services/models/api-response';
import { relativeTimeRounding } from 'moment-timezone';
import { Column } from 'src/app/layout/table/table.types';
/* -------------------------------------------------------------------------- */


@Component({
  selector: 'cmdb-object-edit',
  templateUrl: './object-edit.component.html',
  styleUrls: ['./object-edit.component.scss']
})
export class ObjectEditComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.Edit;
  public objectInstance: CmdbObject;
  public typeInstance: CmdbType;
  public renderResult: RenderResult;
  public renderForm: UntypedFormGroup;
  public commitForm: UntypedFormGroup;
  private objectID: number;
  public activeState: boolean;


  public selectedLocation: number = -1;
  public locationTreeName: string;
  public locationForObjectExists: boolean = false;

  // Table Template: Type actions column
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

  public fields: Array<any> = [];
  // Table columns definition
  columns: Array<Column> = [];

  /* -------------------------------------------------------------------------- */
  /*                                 LIFE CYCLE                                 */
  /* -------------------------------------------------------------------------- */

  constructor(private objectService: ObjectService,
    private typeService: TypeService,
    private route: ActivatedRoute,
    private router: Router,
    private toastService: ToastService,
    private locationService: LocationService,
    private sidebarService: SidebarService,
    private _location: Location) {
    this.route.params.subscribe((params) => {
      this.objectID = params.publicID;
    });

    this.renderForm = new UntypedFormGroup({});
    this.commitForm = new UntypedFormGroup({
      comment: new UntypedFormControl('')
    });
  }


  public ngOnInit(): void {
    this.objectService.getObject(this.objectID).subscribe((rr: RenderResult) => {
      this.renderResult = {
        ...rr, sections: rr.sections.filter(sec => sec.type !== 'multi-data-section')
      }
      this.activeState = this.renderResult.object_information.active;
    },
      error => {
        console.error(error);
      },
      () => {
        this.objectService.getObject<CmdbObject>(this.objectID, true).subscribe(ob => {
          this.objectInstance = ob;
        });

        this.typeService.getType(this.renderResult.type_information.type_id).subscribe((value: CmdbType) => {
          this.typeInstance = value;
          this.fields = value.fields
          this.isMultiDataSection(value.render_meta?.sections, value.fields)
        });
      });
  }


  /**
   * Determines if a section is a multi-data section and generates corresponding columns for display.
   * 
   * @param sectionFields Array of fields describing the section
   * @param fields Array of all available fields
   */
  isMultiDataSection(sectionFields, fields) {

    let actionsColumn: Column = {
      display: 'Actions',
      name: 'actions',
      data: 'actions',
      searchable: false,
      sortable: false,
      fixed: true,
      template: this.actionsTemplate,
      cssClasses: ['text-center'],
      cellClasses: ['actions-buttons']
    };

    this.columns = sectionFields
      .filter(field => field.type === 'multi-data-section')
      .map(field => {
        const filteredFields = fields.filter(fld => field.fields.includes(fld.name));

        // Map the filtered fields to columns
        const columns = filteredFields.map(fld => ({
          display: fld.label,
          name: fld.name,
          type: fld.type,

        }));

        return columns;
      })
      .flat();

    this.columns.push(actionsColumn);

  }


  @HostListener('window:scroll', ['$event'])
  onWindowScroll($event) {
    const dialog = document.getElementById('object-form-action');
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      dialog.style.visibility = 'visible';
    } else {
      dialog.style.visibility = 'hidden';
    }
  }

  /**
   * Function to handle navigating back in the browser history
  */
  backClicked() {
    this._location.back();
  }


  public editObject(): void {
    this.renderForm.markAllAsTouched();
    if (this.renderForm.valid) {
      const patchValue = [];

      Object.keys(this.renderForm.value).forEach((key: string) => {
        let val = this.renderForm.value[key];

        if (key == 'dg_location') {
          this.selectedLocation = val;
        }
        else if (key == 'locationTreeName') {
          this.locationTreeName = val;
          return;
        } else if (key == 'locationForObjectExists') {
          this.locationForObjectExists = String(val).toLowerCase() === 'true' ? true : false;
          return;
        }

        if (val === undefined || val == null) {
          val = '';

          if (key == "dg_location") {
            patchValue.push({
              name: key,
              value: null
            });
          }

        } else {
          patchValue.push({
            name: key,
            value: val
          });
        }
      });

      this.handleLocation(this.objectInstance.public_id, this.selectedLocation, this.locationTreeName, this.objectInstance.type_id);

      this.objectInstance.fields = patchValue;
      this.objectInstance.comment = this.commitForm.get('comment').value;
      this.objectInstance.active = this.activeState;
      this.objectService.putObject(this.objectID, this.objectInstance).subscribe((res: APIUpdateMultiResponse) => {
        if (res.failed.length === 0) {
          this.objectService.changeState(this.objectID, this.activeState).subscribe((resp: boolean) => {
            this.sidebarService.ReloadSideBarData();
            this.toastService.success('Object was successfully updated!');
            this.router.navigate(['/framework/object/view/' + this.objectID]);
          });
        } else {
          for (const err of res.failed) {
            this.toastService.error(err.error_message);
          }
          this.router.navigate(['/framework/object/type/' + this.objectInstance.type_id]);
        }
      }, error => {
        this.toastService.error(error);
        this.router.navigate(['/framework/object/type/' + this.objectInstance.type_id]);
      });
    }
  }


  public toggleChange() {
    this.activeState = this.activeState !== true;
    this.renderForm.markAsDirty();
  }


  private handleLocation(object_id: number, parent: number, name: string = "", type_id: number) {
    let params = {
      "object_id": object_id,
      "parent": parent,
      "name": name,
      "type_id": type_id
    }

    //a parent is selected and there is no existing location for this object => create it
    if (parent && parent > 0 && !this.locationForObjectExists) {
      this.locationService.postLocation(params).subscribe((res: APIUpdateMultiResponse) => {
      }, error => {
        this.toastService.error(error);
      });
      return;
    }

    //a parent is selected and location for this object exists => update existing location
    if (parent && parent > 0 && this.locationForObjectExists) {
      this.locationService.updateLocationForObject(params).subscribe((res: APIUpdateMultiResponse) => {
      }, error => {
        this.toastService.error(error);
      });
      return;
    }

    //parent is removed but location still exists => delete location
    if (!parent && this.locationForObjectExists) {
      this.locationService.deleteLocationForObject(object_id).subscribe((res: APIUpdateMultiResponse) => {
      }, error => {
        this.toastService.error(error);
      });
      return;
    }
  }
}
