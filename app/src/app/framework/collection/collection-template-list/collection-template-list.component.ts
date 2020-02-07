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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { CollectionService } from '../../services/collection.service';
import { CmdbCollectionTemplate } from '../../models/cmdb-collection';
import { Subscription } from 'rxjs';

@Component({
  selector: 'cmdb-collection-template-list',
  templateUrl: './collection-template-list.component.html',
  styleUrls: ['./collection-template-list.component.scss']
})
export class CollectionTemplateListComponent implements OnInit, OnDestroy {

  private collectionTemplateListSubscription: Subscription;
  public collectionTemplateList: CmdbCollectionTemplate[] = [];

  constructor(private collectionService: CollectionService) {
    this.collectionTemplateListSubscription = new Subscription();
  }

  public ngOnInit(): void {
    // Load complete list
    this.collectionTemplateListSubscription = this.collectionService.getCollectionTemplateList().
    subscribe((collectionTemplateList: CmdbCollectionTemplate[]) => {
      this.collectionTemplateList = collectionTemplateList;
    });
  }

  public ngOnDestroy(): void {
    this.collectionTemplateListSubscription.unsubscribe();
  }

}
