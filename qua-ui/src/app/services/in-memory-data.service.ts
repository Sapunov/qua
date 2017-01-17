import { InMemoryDbService } from 'angular-in-memory-web-api';

export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    let search = {
      query: 'Text query',
      hits: [
        {
          id: 1,
          title: 'One question',
          snippet: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatum nostrum perferendis molestiae! Tenetur ipsa voluptatem cum in? Optio commodi, magnam quidem eius sapiente dignissimos. Excepturi, culpa, nulla! Veritatis corporis fuga repudiandae natus unde cum, delectus officiis quidem possimus, et blanditiis tempora reprehenderit, laboriosam quos aliquam omnis odio autem nam. Quae animi similique nisi necessitatibus, blanditiis labore doloremque eum ea accusamus laborum adipisci fugiat, laudantium eos delectus quo esse vero quos totam ipsam amet, explicabo earum tempora. Inventore in dolores quis provident consectetur eius non praesentium quidem! Eius repudiandae commodi possimus saepe ea reprehenderit et, sed aliquid, tempore pariatur modi, eligendi.',
          image: '/',
          score: 8.1,
          category: {
            id: 1,
            name: 'category_name_1'
          }
        },
        {
          id: 2,
          title: 'two question',
          snippet: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatum nostrum perferendis molestiae! Tenetur ipsa voluptatem cum in? Optio commodi, magnam quidem eius sapiente dignissimos. Excepturi, culpa, nulla! Veritatis corporis fuga repudiandae natus unde cum, delectus officiis quidem possimus, et blanditiis tempora reprehenderit, laboriosam quos aliquam omnis odio autem nam. Quae animi similique nisi necessitatibus, blanditiis labore doloremque eum ea accusamus laborum adipisci fugiat, laudantium eos delectus quo esse vero quos totam ipsam amet, explicabo earum tempora. Inventore in dolores quis provident consectetur eius non praesentium quidem! Eius repudiandae commodi possimus saepe ea reprehenderit et, sed aliquid, tempore pariatur modi, eligendi.',
          image: '/',
          score: 2.1,
          category: {
            id: 1,
            name: 'category_name_1'
          }
        },
        {
          id: 3,
          title: 'Three question',
          snippet: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatum nostrum perferendis molestiae! Tenetur ipsa voluptatem cum in? Optio commodi, magnam quidem eius sapiente dignissimos. Excepturi, culpa, nulla! Veritatis corporis fuga repudiandae natus unde cum, delectus officiis quidem possimus, et blanditiis tempora reprehenderit, laboriosam quos aliquam omnis odio autem nam. Quae animi similique nisi necessitatibus, blanditiis labore doloremque eum ea accusamus laborum adipisci fugiat, laudantium eos delectus quo esse vero quos totam ipsam amet, explicabo earum tempora. Inventore in dolores quis provident consectetur eius non praesentium quidem! Eius repudiandae commodi possimus saepe ea reprehenderit et, sed aliquid, tempore pariatur modi, eligendi.',
          image: '/',
          score: 18.1,
          category: {
            id: 2,
            name: 'category_name_2'
          }
        },
        {
          id: 4,
          title: 'Four question',
          snippet: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatum nostrum perferendis molestiae! Tenetur ipsa voluptatem cum in? Optio commodi, magnam quidem eius sapiente dignissimos. Excepturi, culpa, nulla! Veritatis corporis fuga repudiandae natus unde cum, delectus officiis quidem possimus, et blanditiis tempora reprehenderit, laboriosam quos aliquam omnis odio autem nam. Quae animi similique nisi necessitatibus, blanditiis labore doloremque eum ea accusamus laborum adipisci fugiat, laudantium eos delectus quo esse vero quos totam ipsam amet, explicabo earum tempora. Inventore in dolores quis provident consectetur eius non praesentium quidem! Eius repudiandae commodi possimus saepe ea reprehenderit et, sed aliquid, tempore pariatur modi, eligendi.',
          image: '/',
          score: 8.1,
          category: {
            id: 2,
            name: 'category_name_2'
          }
        }
      ],
      total: 299,
      category_assumptions: [
        {
          id: 34,
          name: 'Category #1',
          score: 45.6
        }
      ]
    };
    return { search };
  }
}
