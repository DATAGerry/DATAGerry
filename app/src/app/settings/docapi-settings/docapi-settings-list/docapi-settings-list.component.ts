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

import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableDirective } from 'angular-datatables';
import { BehaviorSubject, Subject, Subscription, timer } from 'rxjs';
import { ToastService } from '../../../layout/toast/toast.service';
import {NgbModal, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import { DocTemplate } from '../../../framework/models/cmdb-doctemplate';
import { DocapiService } from '../../../docapi/docapi.service';
import { GeneralModalComponent } from '../../../layout/helpers/modals/general-modal/general-modal.component';

@Component({
  selector: 'cmdb-docapi-settings-list',
  templateUrl: './docapi-settings-list.component.html',
  styleUrls: ['./docapi-settings-list.component.scss']
})
export class DocapiSettingsListComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public docTemplateList: BehaviorSubject<DocTemplate[]> = new BehaviorSubject<DocTemplate[]>([]);
  private subscription: Subscription;
  private modalRef: NgbModalRef;


  constructor(private docapiService: DocapiService, private router: Router,
              private toast: ToastService, private modalService: NgbModal) { }

  ngOnInit() {
    this.dtOptions = {
      order: [2, 'desc'],
      ordering: true,
      stateSave: true,
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.subscription = timer(0, 30000).subscribe(result => {
      this.docapiService.getDocTemplateList().subscribe((list: DocTemplate[]) => {
        this.docTemplateList.next(list);
        this.rerender();
      });
    });
  }

  private rerender(): void {
   if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
        this.dtTrigger.next();
      });
    } else {
      this.dtTrigger.next();
    }
  }

  public delDocTemplate(publicId: number): void {
    this.modalRef = this.modalService.open(GeneralModalComponent);
    this.modalRef.componentInstance.title = 'Delete Document Template';
    this.modalRef.componentInstance.modalMessage = 'Are you sure you want to delete this Document Template?';
    this.modalRef.componentInstance.buttonDeny = 'Cancel';
    this.modalRef.componentInstance.buttonAccept = 'Delete';
    this.modalRef.result.then((result) => {
      if (result) {
        this.docapiService.deleteDocTemplate(publicId).subscribe(resp => console.log(resp),
          error => {},
          () => this.docapiService.getDocTemplateList().subscribe((list: DocTemplate[]) => {
            this.docTemplateList.next(list);
          }));
      }
    });
  }

  ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    this.subscription.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }
}
