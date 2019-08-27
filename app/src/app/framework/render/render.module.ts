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

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RenderElementComponent } from './render-element/render-element.component';
import { TextComponent } from './fields/text/text.component';
import { DummyComponent } from './fields/dummy/dummy.component';
import { RenderComponent } from './render.component';
import { PasswordComponent } from './fields/text/password.component';
import { EmailComponent } from './fields/text/email.component';
import { PhoneComponent } from './fields/text/phone.component';
import { HrefComponent } from './fields/text/href.component';
import { RadioComponent } from './fields/choice/radio.component';
import { SelectComponent } from './fields/choice/select.component';
import { RefComponent } from './fields/special/ref.component';
import { CheckboxComponent } from './fields/choice/checkbox.component';
import { TextareaComponent } from './fields/textarea/textarea.component';
import { LayoutModule } from '../../layout/layout.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ModeErrorComponent } from './components/mode-error/mode-error.component';
import { RenderErrorComponent } from './components/render-error/render-error.component';
import { TextSimpleComponent } from './simple/text/text-simple.component';
import { PasswordSimpleComponent } from './simple/text/password-simple.component';
import { CheckboxSimpleComponent } from './simple/choice/checkbox-simple.component';
import { RadioSimpleComponent } from './simple/choice/radio-simple.component';
import { SelectSimpleComponent } from './simple/choice/select-simple.component';
import { RouterModule } from '@angular/router';


@NgModule({
  entryComponents: [
    TextComponent,
    PasswordComponent,
    DummyComponent,
    EmailComponent,
    PhoneComponent,
    HrefComponent,
    RadioComponent,
    SelectComponent,
    RefComponent,
    CheckboxComponent,
    TextareaComponent,
    TextSimpleComponent,
    PasswordSimpleComponent,
    CheckboxSimpleComponent,
    RadioSimpleComponent,
    SelectSimpleComponent,
    RenderComponent,
    RenderElementComponent
  ],
  declarations: [
    RenderComponent, RenderElementComponent, TextComponent, DummyComponent, PasswordComponent, EmailComponent, PhoneComponent,
    HrefComponent, RadioComponent, SelectComponent, RefComponent, CheckboxComponent, TextareaComponent, ModeErrorComponent,
    RenderErrorComponent, TextSimpleComponent, PasswordSimpleComponent, CheckboxSimpleComponent, RadioSimpleComponent, SelectSimpleComponent
  ],
  exports: [
    RenderElementComponent,
    RenderComponent
  ],
  imports: [
    CommonModule,
    LayoutModule,
    NgbModule,
    NgSelectModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule
  ]
})
export class RenderModule {
}
