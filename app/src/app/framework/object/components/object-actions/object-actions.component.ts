import { Component, Input } from '@angular/core';
import { ObjectService } from '../../../services/object.service';
import { Router } from '@angular/router';
import { ApiCallService } from '../../../../services/api-call.service';
import { CmdbObject } from '../../../models/cmdb-object';
import { CmdbType } from '../../../models/cmdb-type';

@Component({
  selector: 'cmdb-object-actions',
  templateUrl: './object-actions.component.html',
  styleUrls: ['./object-actions.component.scss']
})
export class ObjectActionsComponent {

  @Input() objectInstance: CmdbObject;
  @Input() typeInstance: CmdbType;

  constructor(private api: ApiCallService, private objectService: ObjectService,  private router: Router) {

  }

  public deleteObject(publicID: number) {
    const modal = this.objectService.openModalComponent(
      'Delete Object',
      'Are you sure you want to delete this Object?',
      'Cancel',
      'Delete');

    modal.result.then((result) => {
      if (result) {
        this.api.callDeleteRoute('/object/' + publicID).subscribe((res: boolean) => {
          if (res) {
            this.router.navigate(['/']);
          }
        });
      }
    });
  }
}
