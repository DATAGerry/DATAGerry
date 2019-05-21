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
import { TextControl } from './controls/text/text.control';
import { Controller, ControlsContent } from './controls/controls.common';
import { DndDropEvent } from 'ngx-drag-drop';
import { SectionControl } from './controls/text/section.control';

@Component({
  selector: 'cmdb-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  private fields: ControlsContent[];
  private sections: any[];

  @Input() builderConfig: any = {};
  private builderControls = [
    new Controller('section', SectionControl),
    new Controller('text', TextControl)
  ];

  ngOnInit() {
    this.fields = [];
    this.sections = [];
  }

  private onDrop(event: DndDropEvent, list: any[]) {
    let index = event.index;
    if (typeof index === 'undefined') {

      index = list.length;
    }
    list.splice(index, 0, event.data);
    console.log(event);
    console.log(list);
  }

  private onDragged(item: any, list: any[]) {
    const index = list.indexOf(item);
    list.splice(index, 1);
  }

  private addField(event: DndDropEvent) {
    this.fields.push(event.data);
  }

  private deleteField(field: ControlsContent) {
    const index: number = this.fields.indexOf(field);
    if (index !== -1) {
      this.fields.splice(index, 1);
    }
  }

}
