/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019-2020 NETHINKS GmbH
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

import {Component, Input, OnDestroy, OnInit, TemplateRef, ViewChild} from '@angular/core';
import { LinkService } from '../../../../services/link.service';
import { CmdbLink } from '../../../../models/cmdb-link';
import { forkJoin, Observable, Subscription } from 'rxjs';
import { RenderResult } from '../../../../models/cmdb-render';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectLinkAddModalComponent } from '../../../modals/object-link-add-modal/object-link-add-modal.component';
import { ObjectService } from '../../../../services/object.service';
import { ObjectLinkDeleteModalComponent } from '../../../modals/object-link-delete-modal/object-link-delete-modal.component';
import { ToastService } from '../../../../../layout/toast/toast.service';
import { Column, Sort, SortDirection } from '../../../../../layout/table/table.types';
@Component({
  selector: 'cmdb-object-links',
  templateUrl: './object-links.component.html',
  styleUrls: ['./object-links.component.scss']
})
export class ObjectLinksComponent implements OnInit, OnDestroy {

  // Data
  private id: number;

  @Input()
  public set objectID(objectID: number) {
    this.id = objectID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLinks();
    }
  }

  public get objectID(): number {
    return this.id;
  }

  // Links
  @Input() public renderResult: RenderResult = undefined;
  public linkList: CmdbLink[] = [];
  private linkPartnerSubscription: Subscription;
  private linkListSubscription: Subscription;
  public partnerObjects: RenderResult[];
  private modalRef: NgbModalRef;


  public columns: Array<Column>;

  @ViewChild('dateTemplate', {static: true}) dateTemplate: TemplateRef<any>;

  @ViewChild('idTemplate', {static: true}) idTemplate: TemplateRef<any>;

  @ViewChild('partnerTemplate', {static: true}) partnerTemplate: TemplateRef<any>;

  @ViewChild('deleteTemplate', {static: true}) deleteTemplate: TemplateRef<any>;

  @ViewChild('summaryTemplate', {static: true}) summaryTemplate: TemplateRef<any>;

  public sort: Sort = {name: 'public_id', order: SortDirection.DESCENDING} as Sort;

  constructor(private linkService: LinkService, private objectService: ObjectService, private modalService: NgbModal,
              private toast: ToastService) {
    this.linkPartnerSubscription = new Subscription();
    this.linkListSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.linkList = [];
    this.setColumns();
  }

  public ngOnDestroy(): void {
    this.linkPartnerSubscription.unsubscribe();
    this.linkListSubscription.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public onShowAddModal(): void {
    this.modalRef = this.modalService.open(ObjectLinkAddModalComponent);
    this.modalRef.componentInstance.primaryRenderResult = this.renderResult;
    this.modalRef.result.then((formData: any) => {
      this.linkService.postLink(formData).subscribe(() => {
          this.toast.success(`Object #${formData.primary} linked with #${formData.secondary}.`);
          this.loadLinks();
        },
        (e) => {
          this.toast.error(`${e.message}`);
        });
    });
  }

  public onShowDeleteModal(linkID: number): void {
    this.modalRef = this.modalService.open(ObjectLinkDeleteModalComponent);
    this.modalRef.componentInstance.publicID = linkID;
    this.modalRef.componentInstance.closeEmitter.subscribe((closeResponse: string) => {
      if (closeResponse === 'deleted') {
        this.loadLinks();
      }
    });
  }

  private loadLinks(): void {
    this.linkList = [];
    this.linkPartnerSubscription = this.linkService.getLinksByPartner(this.objectID).subscribe(
      (resp: CmdbLink[]) => {
        this.linkList = resp;
      },
      (error) => console.error(error),
      () => this.loadPartnerObjects()
    );
  }

  private loadPartnerObjects(): void {
    const partnerObservableList: Observable<RenderResult>[] = [];
    for (const link of this.linkList) {
      const partnerID = this.linkService.getPartnerID(this.objectID, link);
      partnerObservableList.push(this.objectService.getObject<RenderResult>(partnerID));
    }
    this.linkListSubscription = forkJoin(partnerObservableList).subscribe(
      (partnerObjects: RenderResult[]) => this.partnerObjects = partnerObjects,
      (error) => console.error(error),
      () => this.insertPartnerObjects()
    );
  }

  public getPartnerObject(link: CmdbLink): RenderResult {
    const partnerID = this.linkService.getPartnerID(this.objectID, link);
    return this.partnerObjects.find(x => x.object_information.object_id === partnerID);
  }

  private insertPartnerObjects() {
    for (const link of this.linkList) {
      link.partnerObject = this.getPartnerObject(link);
    }
  }

  private setColumns(): void {

    const columns = [];

    columns.push({
      display: 'Link ID',
      name: 'link-id',
      data: 'public_id',
      template: this.idTemplate,
      sortable: false,
      searchable: false,
      fixed: true,
      cssClasses: ['text-center'],
      style: {width: '6em', 'font-weight': 'bold'}
    } as unknown as Column);

    columns.push({
      display: 'Partner',
      name: 'partner',
      template: this.partnerTemplate,
      sortable: false,
      searchable: false,
      fixed: true,
      cssClasses: ['text-center'],
      style: {width: '6em'}
    } as unknown as Column);

    columns.push({
      display: 'Summary',
      name: 'summary',
      template: this.summaryTemplate,
      sortable: false,
      searchable: false,
      fixed: true,
      cssClasses: ['text-center'],
      style: {width: '6em'}
    } as unknown as Column);

    columns.push({
      display: 'Creation time',
      name: 'creation-time',
      data: 'creation_time',
      sortable: false,
      searchable: false,
      template: this.dateTemplate,
      fixed: true,
      cssClasses: ['text-center'],
      style: {width: '6em'}
    } as unknown as Column);

    columns.push({
      display: 'Action',
      name: 'action',
      data: 'public_id',
      template: this.deleteTemplate,
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      style: {width: '6em' }
    } as unknown as Column);

    this.columns = columns;
  }
}
