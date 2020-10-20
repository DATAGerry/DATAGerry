import { Component, OnDestroy, OnInit } from '@angular/core';
import { SystemService } from '../system.service';
import { Subject } from 'rxjs';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-properties',
  templateUrl: './properties.component.html',
  styleUrls: ['./properties.component.scss']
})
export class PropertiesComponent implements OnInit, OnDestroy {

  public config: {
    path: string,
    properties: any[]
  };

  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private systemService: SystemService, private toast: ToastService) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: false,
      columnDefs: [
        {
          targets: [0],
          visible: false
        }
      ],
      rowGroup: {
        dataSrc: 0
      }
      ,
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.systemService.getConfigInformation().subscribe(config => {
        this.config = {
          path: config.path,
          properties: []
        };
        for (const section of config.properties) {
          for (const prop of section[1]) {
            this.config.properties.push({
              section: section[0],
              key: prop[0],
              value: prop[1]
            });
          }
        }
      },
      (error) => {
        console.error(error);
      },
      () => {
        this.dtTrigger.next();
      });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
