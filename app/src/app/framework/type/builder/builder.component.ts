/*
* dataGerry - OpenSource Enterprise CMDB
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
import { Controller } from './controls/controls.common';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { SectionControl } from './controls/section.control';
import { UserService } from '../../../user/services/user.service';
import { Group } from '../../../user/models/group';
import { User } from '../../../user/models/user';
import { TextControl } from './controls/text/text.control';
import { PasswordControl } from './controls/text/password.control';
import { EmailControl } from './controls/text/email.control';
import { TelControl } from './controls/text/tel.control';
import { TextAreaControl } from './controls/textarea/textarea.control';
import { LinkControl } from './controls/text/href.control';
import { ReferenceControl } from './controls/specials/ref.control';
import { RadioControl } from './controls/choice/radio.control';
import { SelectControl } from './controls/choice/select.control';
import { CheckboxControl } from './controls/choice/checkbox.control';

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  public sections: any[];
  public userList: User[] = [];
  public groupList: Group[] = [];

  @Input() builderConfig: any = {};

  public structureControls = [
    new Controller('section', SectionControl)
  ];
  public basicControls = [
    new Controller('text', TextControl),
    new Controller('password', PasswordControl),
    new Controller('email', EmailControl),
    new Controller('tel', TelControl),
    new Controller('textarea', TextAreaControl),
    new Controller('href', LinkControl),
    new Controller('checkbox', CheckboxControl),
    new Controller('radio', RadioControl),
    new Controller('select', SelectControl),
  ];
  public specialControls = [
    new Controller('ref', ReferenceControl)
  ];

  public constructor(private userService: UserService) {
    this.userService.getGroupList().subscribe((gList: Group[]) => {
      this.groupList = gList;
    });
    this.userService.getUserList().subscribe((uList: User[]) => {
      this.userList = uList;
    });
  }

  public ngOnInit(): void {
    this.sections = [];
  }

  public onDrop(event: DndDropEvent, list: any[]) {
    if (list
      && (event.dropEffect === 'copy'
        || event.dropEffect === 'move')) {

      let index = event.index;

      if (typeof index === 'undefined') {

        index = list.length;
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
}
