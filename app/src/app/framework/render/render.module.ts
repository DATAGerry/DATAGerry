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
import { LocationComponent } from './fields/special/location.component';
import { CheckboxComponent } from './fields/choice/checkbox.component';
import { TextareaComponent } from './fields/textarea/textarea.component';
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
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RefSimpleComponent } from './simple/special/ref-simple.component';
import { LocationSimpleComponent } from './simple/special/location-simple.component';
import { DateComponent } from './fields/date/date.component';
import { DateSimpleComponent } from './simple/date/date-simple.component';
import { NumberComponent } from './fields/math/number.component';
import { InputAppendsComponent } from './components/input-appends/input-appends.component';
import { ObjectBulkInputAppendsComponent } from './components/object-bulk-input-appends/object-bulk-input-appends.component';
import { RenderFieldComponent } from './fields/components.fields';
import { RefSectionComponent } from './fields/section/ref-section.component';
import { FieldSectionComponent } from './sections/field-section/field-section.component';
import { BaseSectionComponent } from './sections/base-section/base-section.component';
import { ReferenceSectionComponent } from './sections/reference-section/reference-section.component';
import { SectionsFactoryComponent } from './sections/sections-factory/sections-factory.component';
import { DateFormatterPipe } from '../../layout/pipes/date-formatter.pipe';
import { RefSectionSimpleComponent } from './simple/special/ref-section-simple.component';

@NgModule({
  imports: [
    CommonModule,
    NgbModule,
    NgSelectModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    FontAwesomeModule,
  ],
  declarations: [
    RenderComponent,
    RenderElementComponent,
    TextComponent,
    DummyComponent,
    PasswordComponent,
    EmailComponent,
    PhoneComponent,
    HrefComponent,
    RadioComponent,
    SelectComponent,
    RefComponent,
    LocationComponent,
    CheckboxComponent,
    TextareaComponent,
    ModeErrorComponent,
    RenderErrorComponent,
    TextSimpleComponent,
    PasswordSimpleComponent,
    CheckboxSimpleComponent,
    RadioSimpleComponent,
    SelectSimpleComponent,
    RefSimpleComponent,
    LocationSimpleComponent,
    DateSimpleComponent,
    DateComponent,
    NumberComponent,
    InputAppendsComponent,
    ObjectBulkInputAppendsComponent,
    RenderFieldComponent,
    RefSectionComponent,
    FieldSectionComponent,
    BaseSectionComponent,
    ReferenceSectionComponent,
    SectionsFactoryComponent,
    DateFormatterPipe,
    RefSectionSimpleComponent
  ],
  exports: [
    RenderElementComponent,
    RenderComponent,
    DateFormatterPipe
  ]
})
export class RenderModule {
}
