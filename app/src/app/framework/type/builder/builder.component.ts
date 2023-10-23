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

import { ChangeDetectionStrategy, Component, EventEmitter, Input, OnDestroy, Output, SimpleChange, SimpleChanges } from '@angular/core';
import { Controller } from './controls/controls.common';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { SectionControl } from './controls/section.control';
import { Group } from '../../../management/models/group';
import { User } from '../../../management/models/user';
import { TextControl } from './controls/text/text.control';
import { PasswordControl } from './controls/text/password.control';
import { TextAreaControl } from './controls/text/textarea.control';
import { ReferenceControl } from './controls/specials/ref.control';
import { LocationControl } from './controls/specials/location.control';
import { RadioControl } from './controls/choice/radio.control';
import { SelectControl } from './controls/choice/select.control';
import { CheckboxControl } from './controls/choice/checkbox.control';
import { CmdbMode } from '../../modes.enum';
import { DateControl } from './controls/date-time/date.control';
import { RefSectionControl } from './controls/ref-section.common';
import { ReplaySubject } from 'rxjs';
import { CmdbType, CmdbTypeSection } from '../../models/cmdb-type';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PreviewModalComponent } from './modals/preview-modal/preview-modal.component';
import { DiagnosticModalComponent } from './modals/diagnostic-modal/diagnostic-modal.component';
import { ValidationService } from '../services/validation.service';

declare var $: any;

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BuilderComponent implements OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public MODES: typeof CmdbMode = CmdbMode;

  @Input() public mode = CmdbMode.View;
  @Input() public groups: Array<Group> = [];
  @Input() public users: Array<User> = [];
  @Input() public types: Array<CmdbType> = [];

  public sections: Array<any> = [];
  public typeInstance: CmdbType;

  public newSections: Array<CmdbTypeSection> = [];
  public newFields: Array<CmdbTypeSection> = [];

  @Input() public valid: boolean = true;
  @Output() public validChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  @Input('typeInstance')
  public set TypeInstance(instance: CmdbType) {
    this.typeInstance = instance;
    if (instance !== undefined) {
      const preSectionList: any[] = [];
      for (const section of instance.render_meta.sections) {
        preSectionList.push(section);
        const fieldBufferList = [];
        for (const field of section.fields) {
          const found = instance.fields.find(f => f.name === field);
          if (found) {
            fieldBufferList.push(found);
          }
        }
        preSectionList.find(s => s.name === section.name).fields = fieldBufferList;
      }
      this.sections = preSectionList;
    }
  }

  public structureControls = [
    new Controller('section', new SectionControl()),
    new Controller('ref-section', new RefSectionControl())
  ];

  public basicControls = [
    new Controller('text', new TextControl()),
    new Controller('password', new PasswordControl()),
    new Controller('textarea', new TextAreaControl()),
    new Controller('checkbox', new CheckboxControl()),
    new Controller('radio', new RadioControl()),
    new Controller('select', new SelectControl()),
    new Controller('date', new DateControl())
  ];

  public specialControls = [
    new Controller('ref', new ReferenceControl()),
    new Controller('location', new LocationControl())
  ];


  public constructor(private modalService: NgbModal, private validationService: ValidationService) {
    this.typeInstance = new CmdbType();
  }

  public isNewSection(section: CmdbTypeSection): boolean {
    return this.newSections.indexOf(section) > -1;
  }

  public isNewField(field: any): boolean {
    return this.newFields.indexOf(field) > -1;
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
    if (this.sections && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {

      let index = event.index;
      if (typeof index === 'undefined') {
        index = this.sections.length;
      }
      for (const el of this.sections) {
        const collapseCard = ($('#' + el.name) as any);
        collapseCard.collapse('hide');
      }
      if (event.dropEffect === 'copy') {
        this.newSections.push(event.data);
      }
      this.sections.splice(index, 0, event.data);
      this.typeInstance.render_meta.sections = [...this.sections];
      if (event.data.type === 'ref-section' && event.dropEffect === 'copy') {
        this.addRefSectionSelectionField(event.data as CmdbTypeSection);
      }
    }
  }

  /**
   * This method checks if the field is used for an external link.
   * @param field
   */
  public externalField(field) {
    const include = { links: [], total: 0 };
    for (const external of this.typeInstance.render_meta.externals) {
      const fields = external.hasOwnProperty('fields') ? Array.isArray(external.fields) ? external.fields : [] : [];
      const found = fields.find(f => f === field.name);
      if (found) {
        if (include.total < 10) {
          include.links.push(external);
        }
        include.total = include.total + 1;
      }
    }
    return include;
  }

  public onFieldDrop(event: DndDropEvent, section: CmdbTypeSection) {
    const fieldData = event.data;
    if (section && (event.dropEffect === 'copy' || event.dropEffect === 'move')) {

      let index = event.index;
      if (typeof index === 'undefined') {
        index = section.fields.length;
      }

      if (event.dropEffect === 'copy') {
        this.newFields.push(fieldData);
      }
      section.fields.splice(index, 0, fieldData);
      this.typeInstance.render_meta.sections = [...this.sections];
      this.typeInstance.fields.push(fieldData);
      this.typeInstance.fields = [...this.typeInstance.fields];
      this.validationService.initializeData(fieldData.name)
    }
  }

  public onFieldDragged(item: any, section: CmdbTypeSection) {
    const sectionIndex = section.fields.indexOf(item);
    // let updatedDraggedFieldName = this.typeInstance.fields[sectionIndex].name;
    console.log('onFieldDragged Section Index', this.typeInstance.fields[sectionIndex].name)
    section.fields.splice(sectionIndex, 1);
    const fieldIndex = this.typeInstance.fields.indexOf(item);
    let updatedDraggedFieldName = this.typeInstance.fields[fieldIndex].name;

    console.log('onFieldDragged field Index', this.typeInstance.fields[fieldIndex].name)

    this.typeInstance.fields.splice(fieldIndex, 1);
    this.typeInstance.fields = [...this.typeInstance.fields];

    console.log('map onFieldDragged', this.validationService.fieldValidity)
    console.log('setting true this field name', updatedDraggedFieldName)
    this.validationService.setIsValid1(updatedDraggedFieldName, true)

  }

  public onDragged(item: any, list: any[], effect: DropEffect) {
    if (effect === 'move') {
      const index = list.indexOf(item);
      list.splice(index, 1);
      this.sections = list;
      this.typeInstance.render_meta.sections = [...this.sections];
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
      this.sections.splice(index, 1);
      this.typeInstance.render_meta.sections.splice(index, 1);
      this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
    }

  }

  public removeField(item: any, section: CmdbTypeSection) {
    const indexField: number = this.typeInstance.fields.indexOf(item);
    console.log('index field delete before', this.typeInstance.fields[indexField], indexField)

    let removedFieldName = this.typeInstance.fields[indexField].name;
    if (indexField > -1) {
      this.typeInstance.fields.splice(indexField, 1);
      console.log('index field after delete', this.typeInstance.fields, indexField)
      this.typeInstance.fields = [...this.typeInstance.fields];
      // this.validationService.updatelabelValidationStatusMaponDeletion(this.typeInstance.fields)
      this.validationService.updateFieldValidityOnDeletion(removedFieldName);

    }

    const sectionFieldIndex = section.fields.indexOf(item);
    if (sectionFieldIndex > -1) {
      section.fields.splice(sectionFieldIndex, 1);
    }
    this.typeInstance.render_meta.sections = [...this.typeInstance.render_meta.sections];
  }

  public replaceAt(array, index, value) {
    const ret = array.slice(0);
    ret[index] = value;
    return ret;
  }

  public openPreview() {
    const previewModal = this.modalService.open(PreviewModalComponent, { scrollable: true });
    previewModal.componentInstance.sections = this.sections;
  }

  public openDiagnostic() {
    const diagnosticModal = this.modalService.open(DiagnosticModalComponent, { scrollable: true });
    diagnosticModal.componentInstance.data = this.sections;
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
      case 'location':
        return 'globe';
      case 'date':
        return 'calendar-alt';
      default:
        return 'font';
    }
  }

}
