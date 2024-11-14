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
import { HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ApiCallService } from 'src/app/services/api-call.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Injectable({
    providedIn: 'root'
})
export class ReportService {
    private readonly servicePrefix = 'reports';
    private options = { params: new HttpParams() };

    constructor(private api: ApiCallService, private toast: ToastService) { }

    public createReport(reportData: {
        report_category_id: number;
        name: string;
        type_id: number;
        selected_fields: string[];
        conditions: any;
        report_query: {};
        predefined: boolean;
    }): Observable<any> {
        // Initialize HttpParams
        let httpParams = new HttpParams();
        for (let key in reportData) {
            let val: string = typeof reportData[key] === 'object' ? JSON.stringify(reportData[key]) : String(reportData[key]);
            httpParams = httpParams.set(key, val);
        }

        // Set the updated params in options
        this.options.params = httpParams;

        // Post request to create report
        return this.api.callPost<any>(this.servicePrefix + '/', reportData, this.options).pipe(
            map((apiResponse: HttpResponse<any>) => apiResponse.body),
            catchError((error) => {

                this.toast.error(error?.error?.message)
                throw error;
            })
        );
    }
}
