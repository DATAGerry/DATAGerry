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
import { BehaviorSubject, Observable, Subject, Subscription } from 'rxjs';
import { CmdbCollectionTemplate } from '../../models/cmdb-collection';
import { CollectionService } from '../../services/collection.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-collection-add',
  templateUrl: './collection-add.component.html',
  styleUrls: ['./collection-add.component.scss']
})
export class CollectionAddComponent implements OnInit, OnDestroy {

  private collectionTemplateListSubscription: Subscription;
  public collectionTemplateList: CmdbCollectionTemplate[] = [];

  private collectionTemplateSubject: BehaviorSubject<CmdbCollectionTemplate>;
  private collectionTemplateObservable: Observable<CmdbCollectionTemplate>;
  private collectionTemplateSubscription: Subscription;
  public collectionTemplate: CmdbCollectionTemplate = undefined;

  public collectionTemplateForm: FormGroup;

  constructor(private collectionService: CollectionService) {
    this.collectionTemplateListSubscription = new Subscription();
    this.collectionTemplateSubscription = new Subscription();
    this.collectionTemplateSubject = new BehaviorSubject<CmdbCollectionTemplate>(undefined);
    this.collectionTemplateForm = new FormGroup({
      collectionTemplateInstance: new FormControl(undefined, Validators.required)
    });
  }

  public ngOnInit(): void {
    this.collectionTemplateListSubscription = this.collectionService.getCollectionTemplateList()
      .subscribe((collectionTemplateList: CmdbCollectionTemplate[]) => {
        this.collectionTemplateList = collectionTemplateList;
      });

    this.collectionTemplateObservable = this.collectionTemplateSubject.asObservable();
    this.collectionTemplateSubscription = this.collectionTemplateObservable.subscribe(
      (collectionTemplate: CmdbCollectionTemplate) => {
      this.collectionTemplate = collectionTemplate;
    });
  }

  public ngOnDestroy(): void {
    this.collectionTemplateListSubscription.unsubscribe();
    this.collectionTemplateSubject.unsubscribe();
    this.collectionTemplateSubscription.unsubscribe();
  }

  public onTemplateUse(): void {
    const collectionTemplateInstance = this.collectionTemplateForm.get('collectionTemplateInstance').value;
    if (this.collectionTemplateForm.valid && collectionTemplateInstance !== undefined) {
      console.log(collectionTemplateInstance);
      this.collectionTemplateSubject.next(collectionTemplateInstance);
    }
  }

}
