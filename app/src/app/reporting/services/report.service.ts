/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { ApiCallService, ApiServicePrefix, resp } from '../../services/api-call.service';
import {
    APIGetMultiResponse,
    APIGetSingleResponse,
    APIInsertSingleResponse,
    APIDeleteSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';

@Injectable({
    providedIn: 'root'
})
export class ReportService<T = any> implements ApiServicePrefix {
    public servicePrefix: string = 'reports';

    public options = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        }),
        params: {},
        observe: resp
    };

    constructor(private api: ApiCallService) { }


    /**
     * Fetches all reports.
     */
    public getAllReports(params: CollectionParameters = {
        filter: '',
        limit: 10,
        sort: 'public_id',
        order: 1,
        page: 1
    }): Observable<APIGetMultiResponse<T>> {
        const options = this.options;
        let httpParams: HttpParams = new HttpParams();

        if (params.filter !== undefined) {
            const filter = JSON.stringify(params.filter);
            httpParams = httpParams.set('filter', filter);
        }

        httpParams = httpParams.set('limit', params.limit.toString());
        httpParams = httpParams.set('sort', params.sort);
        httpParams = httpParams.set('order', params.order.toString());
        httpParams = httpParams.set('page', params.page.toString());
        options.params = httpParams;

        return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
            map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => apiResponse.body)
        );
    }


    /**
     * Fetches a single report by its public ID.
     */
    public getReportById(publicID: number): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callGet<T>(`${this.servicePrefix}/${publicID}`, options).pipe(
            map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => apiResponse.body.result as T)
        );
    }


    /**
     * Creates a new report.
     */
    public createReport(reportData: {
        report_category_id: number;
        name: string;
        type_id: number;
        selected_fields: string[];
        conditions: any;
        report_query: {};
        predefined: boolean;
    }): Observable<T> {
        let httpParams = new HttpParams();
        for (let key in reportData) {
            let val: string = typeof reportData[key] === 'object' ? JSON.stringify(reportData[key]) : String(reportData[key]);
            httpParams = httpParams.set(key, val);
        }

        this.options.params = httpParams;

        return this.api.callPost<T>(this.servicePrefix + '/', reportData, this.options).pipe(
            map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => apiResponse.body.raw as T),
            catchError((error) => {
                throw error;
            })
        );
    }


    /**
     * Deletes a report by its public ID.
     */
    public deleteReport(publicID: number): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callDelete<T>(`${this.servicePrefix}/${publicID}`, options).pipe(
            map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => apiResponse.body.raw as T)
        );
    }


    /**
     * Runs a report by its public ID.
     */
    public runReport(publicID: number): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callGet<T>(`${this.servicePrefix}/${publicID}/run`, options).pipe(
            map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => apiResponse.body.result as T)
        );
    }
}