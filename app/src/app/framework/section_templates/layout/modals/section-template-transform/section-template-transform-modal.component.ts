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
import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { CmdbSectionTemplate } from 'src/app/framework/models/cmdb-section-template';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
  selector: 'cmdb-section-template-transform-modal',
  templateUrl: './section-template-transform-modal.component.html',
  styleUrls: ['./section-template-transform-modal.component.scss']
})
export class SectionTemplateTransformModalComponent {

  @Input() 
  public sectionTemplate: CmdbSectionTemplate;

  constructor(public activeModal: NgbActiveModal) {
  }
}