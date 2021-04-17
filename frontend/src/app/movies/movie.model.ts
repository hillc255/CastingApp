export class Movie {
  constructor(
    public _id?: number,
    public title?: string,
    public release_date?: Date,
    public movie_img?: string,
    public movie_publish?: boolean,
  ) { }
}