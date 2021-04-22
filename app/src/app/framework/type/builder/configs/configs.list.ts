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


import { TextFieldEditComponent } from './text/text-field-edit.component';
import { SectionFieldEditComponent } from './section/section-field-edit.component';
import { TextareaEditComponent } from './text/textarea-edit.component';
import { RefFieldEditComponent } from './edits/ref-field-edit.component';
import { ChoiceFieldEditComponent } from './edits/choice-field-edit.component';
import { CheckFieldEditComponent } from './edits/check-field-edit.component';
import { DateFieldEditComponent } from './edits/date-field-edit.component';
import { SectionRefFieldEditComponent } from './section/section-ref-field-edit.component';

export const configComponents: { [type: string]: any } = {
  text: TextFieldEditComponent,
  password: TextFieldEditComponent,
  email: TextFieldEditComponent,
  href: TextFieldEditComponent,
  tel: TextFieldEditComponent,
  section: SectionFieldEditComponent,
  textarea: TextareaEditComponent,
  ref: RefFieldEditComponent,
  checkbox: CheckFieldEditComponent,
  radio: ChoiceFieldEditComponent,
  select: ChoiceFieldEditComponent,
  date: DateFieldEditComponent,
  'ref-section': SectionRefFieldEditComponent,
};
