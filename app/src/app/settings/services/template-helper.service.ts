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

import { Injectable } from '@angular/core';
import { TypeService } from '../../framework/services/type.service';
import { CmdbType } from '../../framework/models/cmdb-type';
import { TemplateHelpdataElement } from '../models/template-helpdata-element';

@Injectable({
  providedIn: 'root'
})
export class TemplateHelperService {

  constructor(private typeService: TypeService) { }

  public getObjectTemplateHelperData(typeId: number, prefix: string = '', iteration: number = 3) {
    let templateHelperData = [];
    templateHelperData.push(<TemplateHelpdataElement>({
      label: 'Public ID',
      templatedata: (prefix ? "{{fields" + prefix + "['id']}}" : "{{id}}")
    }));
    this.typeService.getType(typeId).subscribe(cmdbTypeObj => {
      for (const field of cmdbTypeObj.fields) {
        if(field.type === "ref" && iteration > 0) {
          iteration = iteration - 1;
          let changedPrefix = (prefix ? prefix + "['fields']['" + field.name + "']" : "['" + field.name + "']");
          templateHelperData.push(<TemplateHelpdataElement>({
            label: field.label,
            subdata: this.getObjectTemplateHelperData(field.ref_types, changedPrefix, iteration)
          }));
        }
        else {
        templateHelperData.push(<TemplateHelpdataElement>({
          label: field.label,
          templatedata: (prefix ? "{{fields" + prefix + "['fields']['" + field.name + "']}}" : "{{fields['" + field.name + "']}}")
          }));
        }
      }
    }, 
    (error) => {
      console.error(error);
    });

    return templateHelperData;
  }
}
