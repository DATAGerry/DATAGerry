import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { LogService } from '../../../services/log.service';
import { CmdbLog } from '../../../models/cmdb-log';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-object-log-list',
  templateUrl: './object-log-list.component.html',
  styleUrls: ['./object-log-list.component.scss']
})
export class ObjectLogListComponent implements OnInit, OnChanges, OnDestroy {

  private id: number;
  @ViewChild(DataTableDirective, {static: true})
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLogList();
    }
  }

  get publicID(): number {
    return this.id;
  }

  public logList: CmdbLog[] = [];

  constructor(private logService: LogService) {
  }

  private loadLogList() {
    this.logService.getLogsByObject(this.publicID).subscribe((logs: CmdbLog[]) => {
      this.logList = logs;
    }, (error) => {
      console.log(error);
    }, () => {
      this.renderTable();
    });
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

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [1, 'desc'],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  public ngOnChanges(changes: SimpleChanges): void {
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
