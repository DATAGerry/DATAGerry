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

import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { LinkService } from '../../../../services/link.service';
import { CmdbLink } from '../../../../models/cmdb-link';
import { forkJoin, Observable, Subject, Subscription } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import { RenderResult } from '../../../../models/cmdb-render';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ObjectLinkAddModalComponent } from '../../../components/modals/object-link-add-modal/object-link-add-modal.component';
import { ObjectService } from '../../../../services/object.service';

@Component({
  selector: 'cmdb-object-links',
  templateUrl: './object-links.component.html',
  styleUrls: ['./object-links.component.scss']
})
export class ObjectLinksComponent implements OnInit, OnDestroy {

  // Data
  private id: number;

  @Input()
  public set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLinks();
    }
  }

  public get publicID(): number {
    return this.id;
  }

  // Links
  @Input() public renderResult: RenderResult = undefined;
  public linkList: CmdbLink[];
  private linkListSubscription: Subscription;
  public partnerObjects: RenderResult[];

  // Table
  @ViewChild(DataTableDirective, { static: true })
  private dtElement: DataTableDirective;
  public readonly dtOptions: any = {
    ordering: true,
    order: [[3, 'asc']],
    language: {
      search: '',
      searchPlaceholder: 'Filter...'
    }
  };
  public dtTrigger: Subject<any>;

  constructor(private linkService: LinkService, private objectService: ObjectService, private modalService: NgbModal) {
    this.linkList = [];
  }

  public ngOnInit(): void {
    this.dtTrigger = new Subject();
    this.linkListSubscription = new Subscription();
  }

  public onShowAddModal(): void {
    const modalRef = this.modalService.open(ObjectLinkAddModalComponent);
    modalRef.componentInstance.primaryRenderResult = this.renderResult;
  }

  private loadLinks(): void {
    console.log('Reload object links');
    this.linkService.getLinksByPartner(this.publicID).subscribe(
      (resp: CmdbLink[]) => this.linkList = resp,
      (error) => console.error(error),
      () => this.loadPartnerObjects()
    );
  }

  private loadPartnerObjects(): void {
    const partnerObservableList: Observable<RenderResult>[] = [];
    for (const link of this.linkList) {
      const partnerID = this.linkService.getPartnerID(this.publicID, link);
      partnerObservableList.push(this.objectService.getObject<RenderResult>(partnerID));
    }
    forkJoin(partnerObservableList).subscribe(
      (partnerObjects: RenderResult[]) => this.partnerObjects = partnerObjects,
      (error) => console.error(error),
      () => this.insertPartnerObjects()
    );
  }

  public getPartnerObject(link: CmdbLink): RenderResult {
    const partnerID = this.linkService.getPartnerID(this.publicID, link);
    return this.partnerObjects.find(x => x.object_information.object_id === partnerID);
  }

  private insertPartnerObjects() {
    for (const link of this.linkList) {
      link.partnerObject = this.getPartnerObject(link);
    }
    this.renderTable();
  }

  private renderTable(): void {
    if (this.dtElement.dtInstance === undefined) {
      this.dtTrigger.next();
    } else {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        dtInstance.destroy();
        this.dtTrigger.next();
      });
    }

  }

  public ngOnDestroy(): void {
    this.linkListSubscription.unsubscribe();
    this.dtTrigger.unsubscribe();
  }
}
