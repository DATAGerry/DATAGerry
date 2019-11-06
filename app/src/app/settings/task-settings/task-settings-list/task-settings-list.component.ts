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
import { DataTableDirective } from 'angular-datatables';
import { BehaviorSubject, Subject } from 'rxjs';
import { TaskService } from '../../services/task.service';
import { Task } from '../../models/task';
import {BreadcrumbItem} from "../../../layout/components/breadcrumb/breadcrumb.model";
import {Router} from "@angular/router";

@Component({
  selector: 'cmdb-task-settings-list',
  templateUrl: './task-settings-list.component.html',
  styleUrls: ['./task-settings-list.component.scss']
})
export class TaskSettingsListComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public taskList: BehaviorSubject<Task[]> = new BehaviorSubject<Task[]>([]);

  constructor(private taskService: TaskService, private router: Router) { }

  ngOnInit() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'desc']],
      dom:
        '<"row" <"col-sm-2" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      buttons: [
        {
          text: '<i class="fas fa-plus"></i> Add',
          className: 'btn btn-success btn-sm mr-1',
          action: function() {
            this.router.navigate(['/settings/task/add']);
          }.bind(this)
        }
      ],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.taskService.getTaskList().subscribe((list: Task[]) => {
      this.taskList.next(list);
      this.dtTrigger.next();
    });
  }

  public run_job_manual(itemID: number) {
    this.taskService.run_task(itemID).subscribe(resp => console.log(resp),
      error => {},
      () => this.taskService.getTaskList().subscribe((list: Task[]) => {
        this.taskList.next(list);
      }));
  }

  public delTask(itemID: number) {
    this.taskService.deleteTask(itemID).subscribe(resp => console.log(resp),
      error => {},
      () => this.taskService.getTaskList().subscribe((list: Task[]) => {
        this.taskList.next(list);
      }));
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }
}
