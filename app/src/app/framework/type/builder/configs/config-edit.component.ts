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

import {
  Component,
  ComponentFactoryResolver,
  ComponentRef,
  Input,
  OnInit,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { configComponents } from './configs.list';
import { Group } from '../../../../management/models/group';
import { User } from '../../../../management/models/user';

@Component({
  selector: 'cmdb-config-edit',
  templateUrl: './config-edit.component.html',
  styleUrls: ['./config-edit.component.scss']
})
export class ConfigEditComponent implements OnInit {

  @Input() data: any;
  @Input() groupList: Group[];
  @Input() userList: User[];
  @ViewChild('fieldConfig', {read: ViewContainerRef, static: true}) container;
  private component: any;
  private componentRef: ComponentRef<any>;

  constructor(private resolver: ComponentFactoryResolver) {
  }

  public ngOnInit(): void {
    this.container.clear();
    this.component = configComponents[this.data.type];

    const factory = this.resolver.resolveComponentFactory(this.component);
    this.componentRef = this.container.createComponent(factory);
    this.componentRef.instance.data = this.data;
    this.componentRef.instance.groupList = this.groupList;
    this.componentRef.instance.userList = this.userList;
  }
}
