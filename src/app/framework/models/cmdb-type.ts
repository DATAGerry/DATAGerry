import { CmdbDao } from './cmdb-dao';


export class CmdbType implements CmdbDao {

  readonly public_id: number;
  public author: string;
  public author_id: number;
  public objects_count;

}
