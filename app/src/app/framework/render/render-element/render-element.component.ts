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

import { Component, ComponentFactoryResolver, ComponentRef, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { fieldComponents } from '../fields/fields.list';
import { RenderField } from '../fields/components.fields';
import { ToastService } from '../../../layout/services/toast.service';
import { FormControl, Validators } from '@angular/forms';
import { CmdbMode } from '../../modes.enum';

@Component({
  selector: 'cmdb-render-element',
  templateUrl: './render-element.component.html',
  styleUrls: ['./render-element.component.scss']
})
export class RenderElementComponent extends RenderField implements OnInit {

  @ViewChild('fieldContainer', {read: ViewContainerRef, static: true}) container;
  private component: any;
  private componentRef: ComponentRef<any>;

  constructor(private resolver: ComponentFactoryResolver, public toast: ToastService) {
    super();
  }

  public ngOnInit(): void {
    this.container.clear();
    this.component = fieldComponents[this.data.type];

    const factory = this.resolver.resolveComponentFactory(this.component);
    this.componentRef = this.container.createComponent(factory);
    this.componentRef.instance.parentFormGroup = this.parentFormGroup;
    this.componentRef.instance.mode = this.mode;
    this.componentRef.instance.data = this.data;
    this.componentRef.instance.toast = this.toast;
    const fieldControl = new FormControl('');
    if (this.data.required) {
      fieldControl.setValidators(Validators.required);
    }
    if (this.mode === CmdbMode.View) {
      fieldControl.disable();
    }
    if (this.mode === CmdbMode.View || this.mode === CmdbMode.Edit) {
      fieldControl.patchValue(this.value);
    }
    this.componentRef.instance.parentFormGroup.addControl(
      this.data.name, fieldControl
    );
  }

}
