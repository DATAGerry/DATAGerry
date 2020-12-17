/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { User } from '../models/user';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { UserService } from '../services/user.service';
import { ReplaySubject } from 'rxjs';
import { CollectionParameters } from '../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { Column, Sort, SortDirection } from '../../layout/table/table.types';
import { DatePipe } from '@angular/common';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { UsersPasswdModalComponent } from './modals/users-passwd-modal/users-passwd-modal.component';
import { GroupService } from '../services/group.service';
import { Group } from '../models/group';
import { ToastService } from '../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Component title h1.
   */
  public readonly title: string = 'User';

  /**
   * Title small.
   */
  public readonly description: string = 'Management';

  /**
   * Table Template: User actions column.
   */
  @ViewChild('addButtonTemplate', { static: true }) public buttonTemplate: TemplateRef<any>;

  /**
   * Table Template: User group column.
   */
  @ViewChild('groupTemplate', { static: true }) public groupTemplate: TemplateRef<any>;

  /**
   * Table Template: User actions column.
   */
  @ViewChild('actionsTemplate', { static: true }) public actionsTemplate: TemplateRef<any>;

  /**
   * Password modal
   */
  private modalRef: NgbModalRef;

  /**
   * Users
   */
  public users: Array<User> = [];

  /**
   * Groups
   */
  public groups: Array<Group> = [];

  /**
   * Is the group currently loading
   */
  public groupLoadingStack: Array<number> = [];

  /**
   * Backend api response
   */
  private apiUsersResponse: APIGetMultiResponse<User>;

  /**
   * Table loading?
   */
  public loading: boolean = false;

  /**
   * Default sort parameter
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Collection params
   */
  public params: CollectionParameters = { filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1 };
  public columns: Array<Column> = [];
  public totalUsers: number;

  constructor(private userService: UserService, private groupService: GroupService, private modalService: NgbModal,
              private toast: ToastService) {

  }

  public getGroupByID(publicID: number): Group {
    return this.groups.find(group => group.public_id === publicID);
  }

  public ngOnInit(): void {
    this.columns = [
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'public_id',
        searchable: true,
        sortable: true
      },
      {
        display: 'Username',
        name: 'user_name',
        data: 'user_name',
        searchable: true,
        sortable: true
      },
      {
        display: 'Firstname',
        name: 'first_name',
        data: 'first_name',
        searchable: true,
        sortable: true
      },
      {
        display: 'Lastname',
        name: 'last_name',
        data: 'last_name',
        searchable: true,
        sortable: true
      },
      {
        display: 'Email',
        name: 'email',
        data: 'email',
        searchable: true,
        sortable: true
      },
      {
        display: 'Registered since',
        name: 'registration_time',
        data: 'registration_time',
        sortable: true,
        searchable: false,
        render(data: any) {
          const date = new Date(data);
          return new DatePipe('en-US').transform(date, 'dd/MM/yyyy - hh:mm:ss').toString();
        }
      },
      {
        display: 'Group',
        name: 'group_id',
        data: 'group_id',
        searchable: false,
        sortable: true,
        template: this.groupTemplate,
        render(data: any) {
          return +data;
        }
      },
      {
        display: 'Actions',
        name: 'actions',
        searchable: false,
        sortable: false,
        fixed: true,
        template: this.actionsTemplate,
        cssClasses: ['text-center'],
        cellClasses: ['actions-buttons']
      }
    ] as Array<Column>;
    this.loadUsersFromApi();
  }

  private loadUsersFromApi(): void {
    this.loading = true;
    this.userService.getUsers(this.params).pipe(takeUntil(this.subscriber)).subscribe((response: APIGetMultiResponse<User>) => {
      this.users = response.results as Array<User>;
      this.totalUsers = response.total;
      this.apiUsersResponse = response;
      this.loading = false;
    });
  }

  public onPasswordChange(user: User): void {
    this.modalRef = this.modalService.open(UsersPasswdModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.user = user;
    this.modalRef.result.then(response => {
        this.userService.changeUserPassword(response.public_id, response.password).subscribe(
          (changedUser: User) => {
            this.toast.success(`Password for user with ID: ${ changedUser.public_id } was changed`);
          },
          (error) => this.toast.error(error)
        );
      }
    );
  }

  /**
   * On table page change.
   * Reload all users.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.params.page = page;
    this.loadUsersFromApi();
  }

  /**
   * On table page size change.
   * Reload all users.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.params.limit = limit;
    this.loadUsersFromApi();
  }

  /**
   * On table search change.
   * Reload all users.
   *
   * @param search
   */
  public onSearchChange(search: any): void {
    if (search) {
      let query;
      query = [];
      const or = [];
      const searchableColumns = this.columns.filter(c => c.searchable);
      // Searchable Columns
      for (const column of searchableColumns) {
        const regex: any = {};
        regex[column.name] = {
          $regex: String(search),
          $options: 'ismx'
        };
        or.push(regex);
      }
      query.push({
        $addFields: {
          public_id: { $toString: '$public_id' }
        }
      });
      or.push({
        public_id: {
          $elemMatch: {
            value: {
              $regex: String(search),
              $options: 'ismx'
            }
          }
        }
      });
      query.push({ $match: { $or: or } });
      this.params.filter = query;
    } else {
      this.params.filter = undefined;
    }
    this.loadUsersFromApi();
  }

  /**
   * On table sort change.
   * Reload all users.
   *
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.params.sort = sort.name;
    this.params.order = sort.order;
    this.loadUsersFromApi();
  }


  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
    this.subscriber.next();
    this.subscriber.complete();
  }

}
