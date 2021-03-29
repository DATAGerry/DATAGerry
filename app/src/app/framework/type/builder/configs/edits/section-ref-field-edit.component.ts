/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { CmdbType, CmdbTypeSection } from '../../../../models/cmdb-type';

@Component({
  selector: 'cmdb-section-ref-field-edit',
  templateUrl: './section-ref-field-edit.component.html',
  styleUrls: ['./section-ref-field-edit.component.scss']
})
export class SectionRefFieldEditComponent extends ConfigEditBaseComponent {

  /**
   * Sections from the selected type.
   */
  public typeSections: Array<CmdbTypeSection> = [];

  /**
   * Selected section
   */
  public selectedSection: CmdbTypeSection;

  constructor() {
    super();
  }

  /**
   * When the selected type change.
   * Reset a selected section.
   * @param type
   */
  public onTypeChange(type: CmdbType): void {
    if (this.data.reference.section_name) {
      this.data.reference.section_name = undefined;
      this.data.reference.selected_fields = undefined;
      this.selectedSection = undefined;
    }
    this.typeSections = this.getSectionsFromType(type.public_id);
  }

  /**
   * Get all sections from a type.
   * @param typeID
   */
  public getSectionsFromType(typeID: number): Array<CmdbTypeSection> {
    return this.types.find(t => t.public_id === typeID).render_meta.sections;
  }

  /**
   * When section selection changed.
   * @param section
   */
  public onSectionChange(section: CmdbTypeSection): void {
    this.selectedSection = section;
    this.data.reference.selected_fields = undefined;
  }

  /**
   * Change the field when the reference changes
   * @param name
   */
  public onNameChange(name: string) {
    const oldName = this.data.name;
    const fieldIdx = this.data.fields.indexOf(`${oldName}-field`);
    const field = this.fields.find(x => x.name === `${oldName}-field`);
    this.data.fields[fieldIdx] = `${name}-field`;
    field.name = `${name}-field`;
  }

}
