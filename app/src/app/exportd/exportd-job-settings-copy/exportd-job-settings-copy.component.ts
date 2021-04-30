import { Component } from '@angular/core';
import { CmdbType } from '../../framework/models/cmdb-type';
import { ExportdJob } from '../../settings/models/exportd-job';
import { CmdbMode } from '../../framework/modes.enum';
import { TypeService } from '../../framework/services/type.service';
import { ExportdJobService } from '../exportd-job.service';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../../management/services/user.service';

@Component({
  selector: 'cmdb-exportd-job-settings-copy',
  templateUrl: './exportd-job-settings-copy.component.html',
  styleUrls: ['./exportd-job-settings-copy.component.scss']
})
export class ExportdJobSettingsCopyComponent {

  public taskID: number;
  public taskInstance: ExportdJob;
  public mode: number = CmdbMode.Create;

  constructor(private typeService: TypeService, private taskService: ExportdJobService,
              private route: ActivatedRoute, private userService: UserService) {
    this.taskInstance = new ExportdJob();
    this.route.params.subscribe((param) => {
      if (param.publicID !== undefined) {
        this.taskService.getTask(param.publicID).subscribe((taskCopy: ExportdJob) => {
          delete taskCopy.public_id;
          // @ts-ignore
          delete taskCopy._id;
          delete taskCopy.last_execute_date;
          this.taskInstance = taskCopy;
          this.taskInstance.state = 'SUCCESSFUL';
          this.taskInstance.author_id = this.userService.getCurrentUser().public_id;
          this.taskInstance.author_name = this.userService.getCurrentUser().user_name;
        });
      }
    });
  }
}
