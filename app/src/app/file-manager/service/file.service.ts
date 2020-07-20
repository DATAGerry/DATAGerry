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
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiCallService, ApiService, httpFileOptions } from '../../services/api-call.service';
import { HttpResponse } from '@angular/common/http';
import { ValidatorService } from '../../services/validator.service';
import { FileMetadata } from '../model/metadata';


const httpOptions = {
  observe: 'response',
  responseType: 'blob'
};


@Injectable({
  providedIn: 'root'
})

export class FileService<T = any> implements ApiService {
  public servicePrefix: string = 'media_file';

  constructor(private api: ApiCallService) {
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
   * Download a file by name
   * @param filename name of the file
   */
  public getFileByName(filename: string) {
    return this.api.callPostRoute(this.servicePrefix + '/download/' + filename, null, httpOptions);
  }

  /**
   * Get a list of files by a regex requirement
   * Works with name
   * @param regex parameter
   */
  public getFilesListByName(regex: string): Observable<T[]> {
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
   * @param filename the category id
   */
  public deleteFile(filename: string): Observable<number> {
    return this.api.callDelete<number>(this.servicePrefix + '/' + filename).pipe(
      map((apiResponse: HttpResponse<number>) => {
        return apiResponse.body;
      })
    );
  }

}
