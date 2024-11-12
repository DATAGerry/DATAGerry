import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { ApiCallService, ApiServicePrefix, resp } from '../../services/api-call.service';
import {
    APIGetMultiResponse,
    APIGetSingleResponse,
    APIInsertSingleResponse,
    APIUpdateSingleResponse,
    APIDeleteSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';

@Injectable({
    providedIn: 'root'
})
export class ReportCategoryService<T = any> implements ApiServicePrefix {
    public servicePrefix: string = 'report_categories';

    public options = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        }),
        params: {},
        observe: resp
    };

    constructor(private api: ApiCallService) { }

    /**
     * Posts a dummy report category to the backend.
     */
    public postDummyCategory(): Observable<T> {
        // const options = this.options;
        // options.params = new HttpParams();

        let httpParams = new HttpParams();

        const dummyData = {
            name: 'Dummy Category',
            predefined: false
        };

        for (let key in dummyData) {
            let val: string = String(dummyData[key]);
            httpParams = httpParams.set(key, val);
        }

        this.options.params = httpParams;




        console.log('Sending dummy data:', dummyData); // Log the data

        return this.api.callPost<T>(this.servicePrefix + '/', dummyData, this.options).pipe(
            map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
                return apiResponse.body.raw as T;
            }),
            catchError((error) => {
                console.error('Error response from server:', error); // Log the error response
                throw error;
            })
        );
    }


    /**
     * Fetches all report categories from the backend.
     */
    public getAllCategories(params: CollectionParameters = { filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1 }): Observable<APIGetMultiResponse<T>> {
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
     * Fetches a single report category by its public ID.
     */
    public getCategoryById(publicID: number): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callGet<T>(`${this.servicePrefix}/${publicID}`, options).pipe(
            map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => apiResponse.body.result as T)
        );
    }

    /**
     * Creates a new report category.
     */
    public createCategory(categoryData: { name: string; predefined: boolean }): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callPost<T>(this.servicePrefix + '/', categoryData, options).pipe(
            map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => apiResponse.body.raw as T)
        );
    }

    /**
     * Updates an existing report category by its public ID.
     */
    public updateCategory(categoryData: { public_id: number; name: string; predefined: boolean }): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callPut<T>(`${this.servicePrefix}/${categoryData.public_id}`, categoryData, options).pipe(
            map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => apiResponse.body.result as T)
        );
    }

    /**
     * Deletes a report category by its public ID.
     */
    public deleteCategory(publicID: number): Observable<T> {
        const options = this.options;
        options.params = new HttpParams();

        return this.api.callDelete<T>(`${this.servicePrefix}/${publicID}`, options).pipe(
            map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => apiResponse.body.raw as T)
        );
    }
}
