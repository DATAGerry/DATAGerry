import { Component, OnInit } from '@angular/core';
import { LogService } from '../../../framework/services/log.service';
import { CmdbLog } from '../../../framework/models/cmdb-log';

@Component({
  selector: 'cmdb-log-object-settings',
  templateUrl: './log-object-settings.component.html',
  styleUrls: ['./log-object-settings.component.scss']
})
export class LogObjectSettingsComponent implements OnInit {

  public activeLogList: CmdbLog[];
  public activeLength: number = 0;
  public deletedLogList: CmdbLog[];
  public deleteLength: number = 0;

  constructor(private logService: LogService) {

  }

  public ngOnInit(): void {
    this.logService.getLogsWithExistingObject().subscribe((activeLogs: CmdbLog[]) => {
      this.activeLogList = activeLogs;
      this.activeLength = this.activeLogList.length;
    });
    this.logService.getLogsWithDeletedObject().subscribe((deletedLogs: CmdbLog[]) => {
      this.deletedLogList = deletedLogs;
      this.deleteLength = this.deletedLogList.length;
    });
  }

}
