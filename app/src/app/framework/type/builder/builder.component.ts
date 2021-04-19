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

import { Component, Input, OnDestroy } from '@angular/core';
import { Controller } from './controls/controls.common';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { SectionControl } from './controls/section.control';
import { Group } from '../../../management/models/group';
import { User } from '../../../management/models/user';
import { TextControl } from './controls/text/text.control';
import { PasswordControl } from './controls/text/password.control';
import { TextAreaControl } from './controls/textarea/textarea.control';
import { ReferenceControl } from './controls/specials/ref.control';
import { RadioControl } from './controls/choice/radio.control';
import { SelectControl } from './controls/choice/select.control';
import { CheckboxControl } from './controls/choice/checkbox.control';
import { CmdbMode } from '../../modes.enum';
import { FormGroup } from '@angular/forms';
import { DateControl } from './controls/date-time/date.control';
import { RefSectionControl } from './controls/ref-section.common';
import { ReplaySubject } from 'rxjs';
import { CmdbType, CmdbTypeSection } from '../../models/cmdb-type';

declare var $: any;

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public form: FormGroup;

  @Input() public mode = CmdbMode.View;
  @Input() public groups: Array<Group> = [];
  @Input() public users: Array<User> = [];
  @Input() public types: Array<CmdbType> = [];

  public sections: Array<any> = [];

  public typeInstance: CmdbType;

  @Input('typeInstance')
  public set TypeInstance(instance: CmdbType) {
    this.typeInstance = instance;
  }

  public structureControls = [
    new Controller('section', SectionControl),
    new Controller('ref-section', RefSectionControl)
  ];

  public basicControls = [
    new Controller('text', TextControl),
    new Controller('password', PasswordControl),
    new Controller('textarea', TextAreaControl),
    new Controller('checkbox', CheckboxControl),
    new Controller('radio', RadioControl),
    new Controller('select', SelectControl),
    new Controller('date', DateControl)
  ];

  public specialControls = [
    new Controller('ref', ReferenceControl)
  ];


  public constructor() {
    this.form = new FormGroup({});
    this.typeInstance = new CmdbType();
  }


  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  private addRefSectionSelectionField(refSection: CmdbTypeSection): void {
    refSection.fields = [];
    refSection.fields.push(`${refSection.name}-field`);
    this.typeInstance.fields.push({
      type: 'ref-section-field',
      name: `${refSection.name}-field`,
      label: refSection.label
    });
    this.typeInstance.fields = [...this.typeInstance.fields];
  }

  private removeRefSectionSelectionField(refSection: CmdbTypeSection): void {
    const index = this.typeInstance.fields.map(x => x.name).indexOf(`${refSection.name}-field`);
    this.typeInstance.fields.splice(index, 1);
    this.typeInstance.fields = [...this.typeInstance.fields];
  }

  public onSectionDrop(event: DndDropEvent): void {
    const sections = this.typeInstance.render_meta.sections;
    if (sections && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {

      let index = event.index;

      if (typeof index === 'undefined') {

        index = sections.length;
      }
      for (const el of sections) {
        const collapseCard = ($('#' + el.name) as any);
        collapseCard.collapse('hide');
      }
      sections.splice(index, 0, event.data);
      this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
      if (event.data.type === 'ref-section') {
        this.addRefSectionSelectionField(event.data as CmdbTypeSection);
      }
    }
  }

  public onFieldDrop(event: DndDropEvent, section: CmdbTypeSection) {
    if (section && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {
      let index = event.index;
      if (typeof index === 'undefined') {
        index = section.fields.length;
      }
      section.fields.splice(index, 0, event.data.name);
      this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
    }
    if (section && event.dropEffect === 'copy') {
      this.typeInstance.fields.push(event.data);
      this.typeInstance.fields = [...this.typeInstance.fields];
    }
  }

  public onFieldDragged(item: any, section: CmdbTypeSection) {
    const index = section.fields.indexOf(item);
    section.fields.splice(index, 1);
  }


  public getFieldBySectionID(name: string): any {
    return this.typeInstance.fields.find(f => f.name === name);
  }

  public onDragged(item: any, list: any[], effect: DropEffect) {

    if (effect === 'move') {
      const index = list.indexOf(item);
      list.splice(index, 1);
    }
  }

  public removeSection(item: CmdbTypeSection) {
    const index: number = this.typeInstance.render_meta.sections.indexOf(item);
    if (index !== -1) {
      if (item.type === 'section') {
        const fields: Array<string> = this.typeInstance.render_meta.sections[index].fields;
        for (const field of fields) {
          const fieldIdx = this.typeInstance.fields.map(x => x.name).indexOf(field);
          if (index !== -1) {
            this.typeInstance.fields.splice(fieldIdx, 1);
          }
        }
        this.typeInstance.fields = [...this.typeInstance.fields];
      } else if (item.type === 'ref-section') {
        this.removeRefSectionSelectionField(item);
      }
      this.typeInstance.render_meta.sections.splice(index, 1);
      this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
    }

  }

  public removeField(item: any, section: CmdbTypeSection) {
    const indexField: number = this.typeInstance.fields.indexOf(item);

    this.typeInstance.fields.splice(indexField, 1);
    this.typeInstance.fields = [...this.typeInstance.fields];

    const sectionFieldIndex = section.fields.indexOf(item.name);
    section.fields.splice(sectionFieldIndex, 1);
    this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
  }

  public matchedType(value: string) {
    switch (value) {
      case 'textarea':
        return 'align-left';
      case 'password':
        return 'key';
      case 'checkbox':
        return 'check-square';
      case 'radio':
        return 'check-circle';
      case 'select':
        return 'list';
      case 'ref':
        return 'retweet';
      case 'date':
        return 'calendar-alt';
      default:
        return 'font';
    }
  }

}
