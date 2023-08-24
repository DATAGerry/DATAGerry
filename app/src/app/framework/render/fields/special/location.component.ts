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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit } from '@angular/core';
import { RenderFieldComponent } from '../components.fields';
import { LocationService } from '../../../services/location.service';
import { RenderResult } from '../../../models/cmdb-render';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectPreviewModalComponent } from '../../../object/modals/object-preview-modal/object-preview-modal.component';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  templateUrl: './location.component.html',
  styleUrls: ['./location.component.scss']
})
export class LocationComponent extends RenderFieldComponent implements OnInit, OnDestroy {
  private modalRef: NgbModalRef;
  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();
  public changedReference: BehaviorSubject<any> = new BehaviorSubject<any>(undefined);
  public protect: boolean = false;

  public currentobjectID: number;

  public locationsList: Array<RenderResult> = [];
  public objectLocation: RenderResult;

  public locationTree = new FormControl('', Validators.required);
  public locationForObjectExists = new FormControl('', Validators.required);
  
  public ref;

  
  /* -------------------------------------------------------------------------- */
  /*                            LIFE CYCLE - SECTION                            */
  /* -------------------------------------------------------------------------- */

  public constructor(private locationService: LocationService, private modalService: NgbModal, private route: ActivatedRoute) {    
    super();
  }

  public ngOnInit(): void {
    this.registerForEventChanges();

    this.setTreeName('');
    this.setLocationExists('false');

    this.currentobjectID = this.route.snapshot.params.publicID;

    if(this.data.reference?.object_id > 0){
      this.locationService.getLocation(this.data.reference?.object_id, false).pipe(takeUntil(this.unsubscribe))
      .subscribe((locationObject: RenderResult) => {
          this.objectLocation = locationObject;
        },
        (error) => {
          console.error(error);
        });
    }

    this.getLocations();
  }

  groupByFn = (item) => item.type_label;
  groupValueFn = (_: string, children: any[]) => ({
    name: children[0].type_label,
    // total: children.length
  })


  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  /* -------------------------------------------------------------------------- */
  /*                              HELPER - SECTION                              */
  /* -------------------------------------------------------------------------- */

  public searchRef(term: string, item: any) {
    term = term.toLocaleLowerCase();
    const value = item.object_information.object_id + item.type_information.type_label + item.summary_line;
    return value.toLocaleLowerCase().indexOf(term) > -1 || value.toLocaleLowerCase().includes(term);
  }

  public showReferencePreview() {
    this.modalRef = this.modalService.open(ObjectPreviewModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.renderResult = this.objectLocation;
  }

  public onTreeNameChanged(currentName){
    this.locationTree.setValue(currentName);
    this.parentFormGroup.value['locationTreeName'] = currentName;
    this.parentFormGroup.markAsDirty();

  }


  /**
   * Get all locations which are selectable as parent
   */
  private getLocations(){
    
    const params: CollectionParameters = {
      filter: [{ $match: { type_selectable: { $eq: true } } }],
      limit: 0, sort: 'public_id', order: 1, page: 1
    };

    this.locationService.getLocations(params).pipe(takeUntil(this.unsubscribe))
          .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
            this.setLocationExists('false');
            this.locationsList = this.extractOwnLocation(apiResponse.results);
          });
  }


  private extractOwnLocation(locations){
    let indexOfOwnLocation: number = -1;

    for(let i = 0; i<locations.length; i++){
      if(locations[i].object_id == this.currentobjectID){
        indexOfOwnLocation = i;
        break;
      }
    }

    if(indexOfOwnLocation != -1){
      let ownLocation = locations.splice(indexOfOwnLocation,1)[0];
      
      this.setTreeName(ownLocation['name']);
      this.setLocationExists('true');
    }

    return locations;
  }

  //removes the selected location when unselecting
  public locationChanged(event){
    if(event == undefined){
      this.data.value = null;
    }
  }


  private setLocationExists(val: string){
      this.locationForObjectExists.setValue(val);
      this.parentFormGroup.value['locationForObjectExists'] = val;
  }


  private setTreeName(val: string){
      this.locationTree.setValue(val);
      this.parentFormGroup.value['locationTreeName'] = val;
  }


  private registerForEventChanges() {
    this.parentFormGroup.valueChanges.subscribe( (event) => {
      this.parentFormGroup.value['locationTreeName'] = this.locationTree.value;
      this.parentFormGroup.value['locationForObjectExists'] = this.locationForObjectExists.value;
    });
  }
}
