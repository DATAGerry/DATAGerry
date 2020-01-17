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

import { TextComponent } from './text/text.component';
import { PasswordComponent } from './text/password.component';
import { EmailComponent } from './text/email.component';
import { PhoneComponent } from './text/phone.component';
import { TextareaComponent } from './textarea/textarea.component';
import { HrefComponent } from './text/href.component';
import { CheckboxComponent } from './choice/checkbox.component';
import { RadioComponent } from './choice/radio.component';
import { SelectComponent } from './choice/select.component';
import { DummyComponent } from './dummy/dummy.component';
import { RefComponent } from './special/ref.component';
import { DateComponent } from './date/date.component';


export const fieldComponents: { [type: string]: any } = {
  text: TextComponent,
  password: PasswordComponent,
  email: EmailComponent,
  tel: PhoneComponent,
  textarea: TextareaComponent,
  number: TextComponent,
  href: HrefComponent,
  checkbox: CheckboxComponent,
  radio: RadioComponent,
  select: SelectComponent,
  ref: RefComponent,
  date: DateComponent,
  debug: DummyComponent
};
