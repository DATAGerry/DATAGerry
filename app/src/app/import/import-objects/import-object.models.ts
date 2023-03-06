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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

export class ImporterFile {
  file: File = undefined;
  fileContent: string | ArrayBuffer = undefined;
  fileFormat: string = undefined;
  fileName: string = '';
}

export class ImporterConfig {
  mapping: {} = {};
  // tslint:disable:variable-name
  type_id: number = undefined;
  start_element: number = 0;
  max_elements: number = 0;
  overwrite_public: boolean = false;
  // tslint:enable
}

export class ImportResponse {
  // tslint:disable:variable-name
  success_imports: any[];
  failed_imports: any[];
  // tslint:enable
}
