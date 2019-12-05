import { Component } from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { ExportdJob } from '../../models/exportd-job';
import { CmdbMode } from '../../../framework/modes.enum';
import { TypeService } from '../../../framework/services/type.service';
import { ExportdJobService } from '../../services/exportd-job.service';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../../../management/services/user.service';

@Component({
  selector: 'cmdb-exportd-job-settings-copy',
  templateUrl: './exportd-job-settings-copy.component.html',
  styleUrls: ['./exportd-job-settings-copy.component.scss']
})
export class ExportdJobSettingsCopyComponent {

  public taskID: number;
  public typeInstance: CmdbType;
  public taskInstance: ExportdJob;

  constructor(private typeService: TypeService, private taskService: ExportdJobService,
              private route: ActivatedRoute, private userService: UserService) {
    this.typeInstance = new CmdbType();
    this.route.params.subscribe((param) => {
      console.log(param);
      if (param.publicID !== undefined) {
        console.log('TEST');
        this.taskService.getTask(param.publicID).subscribe((taskCopy: ExportdJob) => {
          this.taskInstance = taskCopy;
          delete this.taskInstance.public_id;
          // @ts-ignore
          delete this.taskInstance._id;
          delete this.taskInstance.last_execute_date;
          this.taskInstance.state = 'SUCCESSFUL';
          this.taskInstance.author_id = this.userService.getCurrentUser().public_id;
          this.taskInstance.author_name = this.userService.getCurrentUser().user_name;
        });
      }
    });
  }
}
