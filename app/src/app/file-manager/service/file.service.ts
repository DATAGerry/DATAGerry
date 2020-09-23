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
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import {
  ApiCallService,
  ApiService,
  httpFileOptions,
} from '../../services/api-call.service';
import { HttpBackend, HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { ValidatorService } from '../../services/validator.service';
import { FileMetadata } from '../model/metadata';
import { FormControl } from '@angular/forms';
import { FileElement } from '../model/file-element';

export const checkFolderExistsValidator = (fileService: FileService, metadata: any, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return fileService.checkFolderExists(control.value, metadata).pipe(
        map((apiResponse: HttpResponse<any[]>) => {
          return apiResponse.body ? { folderExists: true } : null;
        }),
        catchError(() => {
          return new Promise(resolve => {
            resolve(null);
          });
        })
      );
    }));
  };
};

export const httpObserveOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  }),
  observe: 'response'
};

const httpOptions = {
  observe: 'response',
  responseType: 'blob'
};

export const PARAMETER = 'params';

@Injectable({
  providedIn: 'root'
})

export class FileService<T = any> implements ApiService {
  public servicePrefix: string = 'media_file';

  constructor(private api: ApiCallService, private http: HttpClient, private backend: HttpBackend) {
  }

  /**
   * Get all files as a list
   */
  public getAllFilesList(params: any): Observable<T[]> {
    httpObserveOptions[PARAMETER] = { metadata: JSON.stringify(params) };
    return this.api.callGet<T[]>(this.servicePrefix + '/', httpObserveOptions).pipe(
      map((apiResponse: HttpResponse<T[]>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Add a new file into the database (GridFS)
   * @param file raw instance
   * @param metadata raw instance
   */
  public postFile(file: File, metadata: FileMetadata): Observable<T> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));
    return this.api.callPost<T>(this.servicePrefix + '/', formData, httpFileOptions).pipe(
      map((apiResponse: HttpResponse<any>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Update file into the database (GridFS)
   * @param file raw instance
   */
  public putFile(file: FileElement): Observable<T> {
    return this.api.callPut<number>(this.servicePrefix + '/', JSON.stringify(file)).pipe(
      map((apiResponse: HttpResponse<T>) => {
        return apiResponse.body;
      })
    );
  }


  /**
   * Download a file by name
   * @param filename name of the file
   * @param metadata raw instance
   */
  public getFileByName(filename: string, metadata) {
    const formData = new FormData();
    formData.append('metadata', JSON.stringify(metadata));
    return this.api.callPost(this.servicePrefix + '/download/' + filename, formData, httpFileOptions);
  }

  /**
   * Get a list of files by a regex requirement
   * Works with name
   * @param regex parameter
   */
  public getFilesListByRegex(regex: string): Observable<T[]> {
    regex = ValidatorService.validateRegex(regex).trim();
    return this.api.callGet<T[]>(this.servicePrefix + '/download/' + encodeURIComponent(regex)).pipe(
      map((apiResponse: HttpResponse<T[]>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  /**
   * Delete a existing files
   * @param fileID the file id
   * @param params metadata raw instance
   */
  public deleteFile(fileID: number, params): Observable<number> {
    httpFileOptions[PARAMETER] = { metadata: JSON.stringify(params) };
    return this.api.callDelete<number>(this.servicePrefix + '/' + fileID, httpFileOptions).pipe(
      map((apiResponse: HttpResponse<number>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Validation: Check folder name for uniqueness
   *  @param folderName must be unique
   *  @param metadata raw instance
   */
  public checkFolderExists(folderName: string, metadata: FileMetadata) {
    httpObserveOptions[PARAMETER] = { metadata: JSON.stringify(metadata) };
    return this.api.callGet<T>(`${ this.servicePrefix }/${ folderName }`, httpObserveOptions);
  }

}
