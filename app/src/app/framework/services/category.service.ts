/*
* dataGerry - OpenSource Enterprise CMDB
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
import { map } from 'rxjs/operators';
import { ApiCallService } from '../../services/api-call.service';
import { CmdbCategory } from '../models/cmdb-category';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  private servicePrefix: string = 'category';
  private categoryList: CmdbCategory[];

  constructor(private api: ApiCallService) {
    this.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    });
  }

  public findCategory(publicID: number): CmdbCategory {
    return this.categoryList.find(category => category.public_id === publicID);
  }

  public getCategoryList() {
    return this.api.callGetRoute<CmdbCategory[]>(this.servicePrefix + '/');
  }

  public getCategoryTree() {
    return this.api.callGetRoute<CmdbCategory[]>(this.servicePrefix + '/tree');
  }

  public postCategory(data: CmdbCategory) {
    return this.api.callPostRoute<CmdbCategory>(this.servicePrefix + '/', data);
  }

  public updateCategory(data) {
    return this.api.callPutRoute<number>(this.servicePrefix + '/', data);
  }


}
