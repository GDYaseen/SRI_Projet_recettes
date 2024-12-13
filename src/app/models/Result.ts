import { Document } from "./Document";
import { Video } from "./Video";

export interface Result {
    documents : Document[],
    videos : Video,
}