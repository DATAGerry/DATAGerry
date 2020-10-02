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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { TypeService } from '../../framework/services/type.service';
import { TemplateHelpdataElement } from '../models/template-helpdata-element';

@Injectable({
  providedIn: 'root'
})
export class TemplateHelperService {

  constructor(private typeService: TypeService) {
  }

  public async getObjectTemplateHelperData(typeId: number, prefix: string = '', iteration: number = 3) {
    const templateHelperData = [];
    templateHelperData.push(({
      label: 'Public ID',
      templatedata: (prefix ? '{{fields' + prefix + '[\'id\']}}' : '{{id}}')
    }) as TemplateHelpdataElement);
    await this.typeService.getType(typeId).subscribe(async cmdbTypeObj => {
        for (const field of cmdbTypeObj.fields) {
          if (field.type === 'ref' && iteration > 0) {
            const changedPrefix = (prefix ? prefix + '[\'fields\'][\'' + field.name + '\']' : '[\'' + field.name + '\']');
            let subdata;

            if (isNaN(field.ref_types)) {
              await this.getObjectTemplateHelperData(field.ref_types, changedPrefix, iteration - 1).then(data => {
                subdata = data;
              });
            } else if (field.ref_types.length === 1) {
              await this.getObjectTemplateHelperData(field.ref_types[0], changedPrefix, iteration - 1).then(data => {
                subdata = data;
              });
            }

            templateHelperData.push(({
              label: field.label,
              subdata
            }) as TemplateHelpdataElement);
          } else {
            templateHelperData.push(({
              label: field.label,
              templatedata: (prefix ? '{{fields' + prefix + '[\'fields\'][\'' + field.name + '\']}}' : '{{fields[\'' + field.name + '\']}}')
            }) as TemplateHelpdataElement);
          }
        }
      },
      (error) => {
        console.error(error);
      });

    return templateHelperData;
  }
}
