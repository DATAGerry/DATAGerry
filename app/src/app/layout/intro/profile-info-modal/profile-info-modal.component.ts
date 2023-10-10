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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component } from '@angular/core';
import { FormGroup, FormControl, ValidatorFn } from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-profile-info-modal',
    templateUrl: './profile-info-modal.component.html',
    styleUrls: ['./profile-info-modal.component.scss']
  })
  export class ProfileInfoModalComponent {
    public selectedBranches :any;
    public allSelections = {};


    constructor(public activeModal: NgbActiveModal){}

    profileForm = new FormGroup({
      'hardware-inventory-profile': new FormControl(false),
      'software-profile': new FormControl(false),
      'contract-management-profile': new FormControl(false),
      'ipam-profile': new FormControl(false)
    },
      this.oneCheckedRequired()
    );


    /**
     * Validator for which checks if at least one checkbox is selected
     * 
     * @returns Error or null
     */
    public oneCheckedRequired(): ValidatorFn {
      return function validate(formGroup: FormGroup) {
        let checked = false;

        Object.keys(formGroup.controls).forEach(key => {
          const control = formGroup.controls[key];
    
          if (control.value === true) {
            checked = true;
          }
        });

        if(!checked){
          return { requireOnetoBeChecked: true };
        }
        
        return null;
      };
    }


    /**
     * Creates the return dict with all selected values
     */
    setProfileSelections(){
        if(Object.keys(this.allSelections).length == 0){
            this.allSelections['branches'] = this.selectedBranches;
        }

        this.allSelections['profiles'] = this.profileForm.value;
    }

  }
