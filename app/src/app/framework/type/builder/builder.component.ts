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

import {Component, Input, OnInit} from '@angular/core';
import {Controller} from './controls/controls.common';
import {DndDropEvent, DropEffect} from 'ngx-drag-drop';
import {SectionControl} from './controls/section.control';
import {UserService} from '../../../management/services/user.service';
import {Group} from '../../../management/models/group';
import {User} from '../../../management/models/user';
import {TextControl} from './controls/text/text.control';
import {PasswordControl} from './controls/text/password.control';
import {TextAreaControl} from './controls/textarea/textarea.control';
import {ReferenceControl} from './controls/specials/ref.control';
import {RadioControl} from './controls/choice/radio.control';
import {SelectControl} from './controls/choice/select.control';
import {CheckboxControl} from './controls/choice/checkbox.control';
import {GroupService} from '../../../management/services/group.service';
import {CmdbMode} from '../../modes.enum';
import {FormGroup} from '@angular/forms';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {PreviewModalComponent} from './modals/preview-modal/preview-modal.component';
import {DiagnosticModalComponent} from './modals/diagnostic-modal/diagnostic-modal.component';
import {DateControl} from './controls/specials/date.control';

declare var $: any;

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  public sections: any[];
  public userList: User[] = [];
  public groupList: Group[] = [];
  @Input() mode = CmdbMode.View;
  public activeEdit: boolean = false;

  @Input() set builderConfig(data) {
    if (data !== undefined) {
      const preSectionList: any[] = [];
      for (const section of data.render_meta.sections) {
        preSectionList.push(section);
        const fieldBufferList = [];
        for (const field of section.fields) {
          fieldBufferList.push(data.fields.find(f => f.name === field));
        }
        preSectionList.find(s => s.name === section.name).fields = fieldBufferList;
      }
      this.sections = preSectionList;
    }
  }

  public structureControls = [
    new Controller('section', SectionControl)
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

  public builderFormGroup: FormGroup;

  public constructor(private userService: UserService, private groupService: GroupService, private modalService: NgbModal) {
    this.groupService.getGroupList().subscribe((gList: Group[]) => {
      this.groupList = gList;
    });
    this.userService.getUserList().subscribe((uList: User[]) => {
      this.userList = uList;
    });
  }

  public ngOnInit(): void {
    this.sections = [];
    this.builderFormGroup = new FormGroup({});
  }

  public onDrop(event: DndDropEvent, list: any[]) {
    if (list && (event.dropEffect === 'copy')) {
      this.activeEdit = true;
    }

    if (list
      && (event.dropEffect === 'copy'
        || event.dropEffect === 'move')) {

      let index = event.index;

      if (typeof index === 'undefined') {

        index = list.length;
      }
      for (const el of list) {
        const collapseCard = ($('#' + el.name) as any);
        collapseCard.collapse('hide');
      }
      list.splice(index, 0, event.data);
    }
  }

  public onDragged(item: any, list: any[], effect: DropEffect) {

    if (effect === 'move') {
      const index = list.indexOf(item);
      list.splice(index, 1);
    }
  }

  public remove(item: any, list: any[]) {
    const index: number = list.indexOf(item);
    if (index !== -1) {
      list.splice(index, 1);
    }
  }

  public openPreview() {
    const previewModal = this.modalService.open(PreviewModalComponent, {scrollable: true});
    previewModal.componentInstance.sections = this.sections;
  }

  public openDiagnostic() {
    const diagnosticModal = this.modalService.open(DiagnosticModalComponent, {scrollable: true});
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
      case 'date':
        return 'calendar-alt';
      default:
        return 'font';
    }
  }
}
