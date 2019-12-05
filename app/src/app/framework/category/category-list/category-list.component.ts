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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { CategoryService } from '../../services/category.service';
import { CmdbCategory } from '../../models/cmdb-category';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import { Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';
import { ModalComponent } from '../../../layout/helpers/modal/modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import {SidebarService} from "../../../layout/services/sidebar.service";

@Component({
  selector: 'cmdb-category-list',
  templateUrl: './category-list.component.html',
  styleUrls: ['./category-list.component.scss']
})
export class CategoryListComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public categoryList: CmdbCategory[] = [];
  public typeList: CmdbType[];

  constructor(public categoryService: CategoryService, public typeService: TypeService,
              private sidebarService: SidebarService, private toast: ToastService,
              private modalService: NgbModal, private router: Router) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'desc']],
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
      this.dtTrigger.next();
    });
  }

  onDelete(publicID: number) {
    const removeModal = this.modalService.open(ModalComponent);
    removeModal.componentInstance.title = 'Delete Category # ' + publicID;
    removeModal.componentInstance.modalMessage = 'Are you sure you want to delete this Category?';
    removeModal.componentInstance.buttonDeny = 'Cancel';
    removeModal.componentInstance.buttonAccept = 'Delete';
    removeModal.result.then((result) => {
      if (result) {
        this.typeService.updateTypeByCategoryID(publicID).subscribe((resp) => {
          console.log(resp);
        }, (error) => { console.log(error); },
          () => {
            this.categoryService.deleteCategory(publicID).subscribe((confirm) => {
              if (confirm === true) {
                this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
                  this.categoryList = list;
                }, (error) => { console.log(error); },
                  () => {
                    this.sidebarService.updateCategoryTree();
                    this.toast.show('Category was deleted');
                });
              }
            });
          });
      }
    }, (reason) => {
      console.log(reason);
    });
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }
}
