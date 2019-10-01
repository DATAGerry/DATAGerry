import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { RightService } from '../../services/right.service';
import { Right } from '../../models/right';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-rights-list',
  templateUrl: './rights-list.component.html',
  styleUrls: ['./rights-list.component.scss']
})
export class RightsListComponent implements OnInit, OnDestroy {

  public rightList: Right[];

  @ViewChild(DataTableDirective, { static: false })
  private dtElement: DataTableDirective;

  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private rightService: RightService) {
    this.dtOptions = {
      ordering: false,
      rowGroup: {
        startRender: (rows, group) => {
          return group + ' (' + rows.count() + ' rights)';
        },
        dataSrc: (data) => {
          const baseData = data[0].split('.');
          return `${baseData[0]}.${baseData[1]}`;
        }
      },
      pageLength: 50
    };
  }

  public ngOnInit(): void {
    this.rightService.getRightList().subscribe((rightList: Right[]) => {
        this.rightList = rightList;
      },
      (error) => {
        console.error(error);
      },
      () => {
        this.dtTrigger.next();
      }
    );
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
    });

  }

}
