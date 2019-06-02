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

export interface ControlsCommon {
  label: string;
  name: string;
  icon?: string;
  dndType: string;

  content(): any;
}

export interface ControlsContent {
  required: boolean;
  name: string;
  helperText: string;
  placeholder: string;
  type: string;
  access: boolean;
  groups: number[];
  users: number[];
  value: any;
  optional: any;

}

export interface StructureContent {
  name: string;
  label: string;
  position: number;
  type: string;
}

export function randomName(desc: string) {
  return `${desc}-${Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000}`;
}


export class Controller {

  private typeController: ControlsCommon;

  constructor(public name: string, public descr: any) {
    this.typeController = new descr();
  }

}
