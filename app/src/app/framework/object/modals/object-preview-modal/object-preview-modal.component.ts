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


import { Component, Input, OnInit } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { CmdbMode } from '../../../modes.enum';
import { FormGroup } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-object-preview-modal',
  templateUrl: './object-preview-modal.component.html',
  styleUrls: ['./object-preview-modal.component.scss']
})
export class ObjectPreviewModalComponent implements OnInit {

  @Input() renderResult: RenderResult;
  public mode = CmdbMode.View;
  public formGroupDummy: FormGroup;

  constructor(public activeModal: NgbActiveModal) {
    this.formGroupDummy = new FormGroup({});
  }

  public ngOnInit(): void {
  }

}
