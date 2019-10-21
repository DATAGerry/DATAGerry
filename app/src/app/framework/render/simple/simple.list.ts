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

import { TextSimpleComponent } from './text/text-simple.component';
import { PasswordSimpleComponent } from './text/password-simple.component';
import { CheckboxSimpleComponent } from './choice/checkbox-simple.component';
import { RadioSimpleComponent } from './choice/radio-simple.component';
import { SelectSimpleComponent } from './choice/select-simple.component';
import { RefSimpleComponent } from './special/ref-simple.component';
import {DateSimpleComponent} from "./date/date-simple.component";

export const simpleComponents: {[type: string]: any} = {
  text: TextSimpleComponent,
  password: PasswordSimpleComponent,
  email: TextSimpleComponent,
  tel: TextSimpleComponent,
  textarea: TextSimpleComponent,
  href: TextSimpleComponent,
  checkbox: CheckboxSimpleComponent,
  radio: RadioSimpleComponent,
  select: SelectSimpleComponent,
  ref: RefSimpleComponent,
  date: DateSimpleComponent,
  debug: TextSimpleComponent
};
