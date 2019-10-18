import { Component, OnDestroy, OnInit } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { User } from '../../../../management/models/user';
import { Subject } from 'rxjs';
import { ObjectService } from '../../../services/object.service';
import { AuthService } from '../../../../auth/services/auth.service';

@Component({
  selector: 'cmdb-user-object-new',
  templateUrl: './user-objects-new.component.html',
  styleUrls: ['./user-objects-new.component.scss']
})
export class UserObjectsNewComponent implements OnInit, OnDestroy {

  public newObjects: RenderResult[] = [];
  public newObjectsLength: number = 0;
  public issuedTokenTime: number;
  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  public constructor(private objectService: ObjectService, private authService: AuthService) {
    this.issuedTokenTime = this.authService.currentUserValue.token_issued_at;
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[3, 'desc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.objectService.getNewObjectsSince(this.issuedTokenTime).subscribe((objectList: RenderResult[]) => {
        this.newObjects = objectList;
        this.newObjectsLength = this.newObjects.length;
      },
      (error) => {
        console.error(error);
        this.newObjectsLength = 0;
        this.dtTrigger.next();
      },
      () => {
        this.dtTrigger.next();
      });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
