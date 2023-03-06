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

import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'fileSize'})
export class FileSizePipe implements PipeTransform {
  transform(size) {
    if (isNaN(size)) {
      size = 0;
    }

    if (size < 1024) {
      return size + ' Bytes';
    }

    size /= 1024;

    if (size < 1024) {
      return size.toFixed(2) + ' Kb';
    }

    size /= 1024;

    if (size < 1024) {
      return size.toFixed(2) + ' Mb';
    }

    size /= 1024;

    if (size < 1024) {
      return size.toFixed(2) + ' Gb';
    }
  }
}
