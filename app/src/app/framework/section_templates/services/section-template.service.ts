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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams } from '@angular/common/http';

import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { ApiCallService, ApiServicePrefix, resp } from 'src/app/services/api-call.service';

import { CmdbSectionTemplate } from '../../models/cmdb-section-template';
/* ------------------------------------------------------------------------------------------------------------------ */

@Injectable({
    providedIn: 'root'
})
export class SectionTemplateService implements ApiServicePrefix {
    public servicePrefix: string = 'section_templates';

    public readonly options = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        }),
        params: {},
        observe: resp
    };



    constructor(private api: ApiCallService) {}

/* -------------------------------------------------- CRUD - CREATE ------------------------------------------------- */

    /**
     * Creates and stores a CmdbLocation in the database
     * 
     * @param objectInstance (CmdbLocation): location which should be crated
     * @returns Observable<any>
     */
    public postSectionTemplate(params): Observable<any> {

            let httpParams = new HttpParams();
      
            for (let key in params){
              let val:string = String(params[key]);
              httpParams = httpParams.set(key, val);
            }

            this.options.params = httpParams;
      
            return this.api.callPost<CmdbSectionTemplate>(this.servicePrefix + '/', params , this.options).pipe(
                map((apiResponse) => {
                    return apiResponse.body;
                }),
            );
        }


  }