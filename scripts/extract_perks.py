import html
import json
from bs4 import BeautifulSoup

raw_data = """{
                &quot;userItems&quot;: [ {
                  &quot;title&quot;: &quot;Roxy’s Emporium&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Buy one gently used book, get one of equal or lesser value FREE! *New books are not included&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit website&quot;,
                    &quot;buttonLink&quot;: &quot;https://roxys-emporiumbooksgiftshadcrafts.business.site&quot;
                  },
                  &quot;imageId&quot;: &quot;610efaab3685a32de630e989&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;610efaab3685a32de630e989&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1628371627258,
                    &quot;updatedOn&quot;: 1628562930367,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1628371627258,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1628371627610-SUWNYDMKSBV6OODB0YSV&quot;,
                    &quot;systemDataVariants&quot;: &quot;883x748,100w,300w,500w,750w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;79709df0-a08d-4032-a85e-83fd166f3717-upload_your_logo-books-3-use-this-one.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;484338&quot;,
                      &quot;topRightAverage&quot;: &quot;523329&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;4d4948&quot;,
                      &quot;bottomRightAverage&quot;: &quot;aea19c&quot;,
                      &quot;centerAverage&quot;: &quot;352c24&quot;,
                      &quot;suggestedBgColor&quot;: &quot;525446&quot;
                    },
                    &quot;urlId&quot;: &quot;gb0l8mmu8i8st27yrvqpav059224yq&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1628371627610-SUWNYDMKSBV6OODB0YSV/79709df0-a08d-4032-a85e-83fd166f3717-upload_your_logo-books-3-use-this-one.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;883x748&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Black River Tavern&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;10% off burgers and pizzas from 8/6/21 – 12/31/21&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Excluding weekday specials&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit website&quot;,
                    &quot;buttonLink&quot;: &quot;https://www.theblackrivertavern.com&quot;
                  },
                  &quot;imageId&quot;: &quot;610f03c4f932a77577d77cf8&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;610f03c4f932a77577d77cf8&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1628373956998,
                    &quot;updatedOn&quot;: 1628562930378,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1628373956998,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1628373957212-0WM56XM1XCIGF3J9PLBA&quot;,
                    &quot;systemDataVariants&quot;: &quot;440x429,100w,300w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;IMG_4205.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;f4d5a9&quot;,
                      &quot;topRightAverage&quot;: &quot;f4d5a9&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;f4d5a9&quot;,
                      &quot;bottomRightAverage&quot;: &quot;f4d5a9&quot;,
                      &quot;centerAverage&quot;: &quot;d0b895&quot;,
                      &quot;suggestedBgColor&quot;: &quot;f4d5a9&quot;
                    },
                    &quot;urlId&quot;: &quot;ygo8hdkcywtfjeemngst21eiojk9r1&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1628373957212-0WM56XM1XCIGF3J9PLBA/IMG_4205.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;440x429&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Sambino's Pizza&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;The Big Sambino” X-Large 2 Topping Pizza + Cheese Bread + 10 Wings and a 2 Liter of Pop for only $28.95!&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;from 8/23/21 to 12/31/21&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;https://www.sambinospizza.com&quot;
                  },
                  &quot;imageId&quot;: &quot;611ce360e5f32005491d4641&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611ce360e5f32005491d4641&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629283168430,
                    &quot;updatedOn&quot;: 1629283170775,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629283168430,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629283168569-J4X93OGYZ0FFDENDD3ND&quot;,
                    &quot;systemDataVariants&quot;: &quot;281x182,100w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;d4e022a2-65d5-4842-8ec1-659fc75ef02a-upload_your_logo-82A1721A-AB67-4CD3-90C4-A747B11B374C.jpeg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;eff1ef&quot;,
                      &quot;topRightAverage&quot;: &quot;f6f5f4&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;e9e9e9&quot;,
                      &quot;bottomRightAverage&quot;: &quot;e9c2c3&quot;,
                      &quot;centerAverage&quot;: &quot;c7d7cc&quot;,
                      &quot;suggestedBgColor&quot;: &quot;efebe5&quot;
                    },
                    &quot;urlId&quot;: &quot;pqjd2rqxsha7eptzp7quqvyj8qy2kf&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629283168569-J4X93OGYZ0FFDENDD3ND/d4e022a2-65d5-4842-8ec1-659fc75ef02a-upload_your_logo-82A1721A-AB67-4CD3-90C4-A747B11B374C.jpeg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;281x182&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Stewart's TV and Appliance&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Spend $500 and get $25 off, spend $1000 and get $50 off.&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;https://www.stewartappliance.com&quot;
                  },
                  &quot;imageId&quot;: &quot;611ce70a97af2d15598b436c&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611ce70a97af2d15598b436c&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629284106649,
                    &quot;updatedOn&quot;: 1629284110396,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629284106649,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629284106999-H19IT4LJ7HLFE42MP88T&quot;,
                    &quot;systemDataVariants&quot;: &quot;562x430,100w,300w,500w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;IMG_4266 2.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;topRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;centerAverage&quot;: &quot;d18a92&quot;,
                      &quot;suggestedBgColor&quot;: &quot;ffffff&quot;
                    },
                    &quot;urlId&quot;: &quot;bmi1fp7tik4z9racofhdmpoj9ojtuo&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629284106999-H19IT4LJ7HLFE42MP88T/IMG_4266+2.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;562x430&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Uncle Al's Pizzeria&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Buy any family-size pizza and receive a second pizza, any size, of equal or lesser value, for 50% off the menu price.&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;https://www.unclealspizzeria.com&quot;
                  },
                  &quot;imageId&quot;: &quot;611d48201eb1ee0f4233622d&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611d48201eb1ee0f4233622d&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629308960618,
                    &quot;updatedOn&quot;: 1629308962609,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629308960618,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629308960742-Z64K1DMNY7HOSA9Y3C2T&quot;,
                    &quot;systemDataVariants&quot;: &quot;549x356,100w,300w,500w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;IMG_4268.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;topRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;centerAverage&quot;: &quot;b2b2b3&quot;,
                      &quot;suggestedBgColor&quot;: &quot;ffffff&quot;
                    },
                    &quot;urlId&quot;: &quot;fxodjbgwcq6ceylkm35sgdsqmikc7i&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629308960742-Z64K1DMNY7HOSA9Y3C2T/IMG_4268.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;549x356&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Attractive Kitchens and Floors&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;$100 Off purchases of $1,000 or more&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Expires 9/30/21&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;https://attractivekitchensandfloors.com&quot;
                  },
                  &quot;imageId&quot;: &quot;611d5ec94c20a561c65a1519&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611d5ec94c20a561c65a1519&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629314761986,
                    &quot;updatedOn&quot;: 1629314768869,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629314761986,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629314762984-2YRMA0E620VW0L0FRBMU&quot;,
                    &quot;systemDataVariants&quot;: &quot;1000x631,100w,300w,500w,750w,1000w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;PNG&quot;,
                    &quot;filename&quot;: &quot;Logo-AttractiveKitchenFloors.png&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;000000&quot;,
                      &quot;topRightAverage&quot;: &quot;000000&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;000000&quot;,
                      &quot;bottomRightAverage&quot;: &quot;000000&quot;,
                      &quot;centerAverage&quot;: &quot;7fb198&quot;,
                      &quot;suggestedBgColor&quot;: &quot;000000&quot;
                    },
                    &quot;urlId&quot;: &quot;ezz5rg8prt6wsm0g9m5khmjgwcuy2s&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629314762984-2YRMA0E620VW0L0FRBMU/Logo-AttractiveKitchenFloors.png&quot;,
                    &quot;contentType&quot;: &quot;image/png&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;1000x631&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Foundry’s Kitchen and Bar&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Daily special&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Expires 9/18/21&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit website&quot;,
                    &quot;buttonLink&quot;: &quot;https://foundrykitchen.bar&quot;
                  },
                  &quot;imageId&quot;: &quot;611d8d933390496f0dd63e8a&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611d8d933390496f0dd63e8a&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629326739693,
                    &quot;updatedOn&quot;: 1629326742616,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629326739693,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629326739798-QMB4R3C8A256LEQE8RW5&quot;,
                    &quot;systemDataVariants&quot;: &quot;550x291,100w,300w,500w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;C49BB502-5BD8-46AF-9A1D-8637A6E1A080.jpeg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;topRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;centerAverage&quot;: &quot;4c4a4b&quot;,
                      &quot;suggestedBgColor&quot;: &quot;ffffff&quot;
                    },
                    &quot;urlId&quot;: &quot;6cb4kb04tsx98ea3zn6htydzau2gi9&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629326739798-QMB4R3C8A256LEQE8RW5/C49BB502-5BD8-46AF-9A1D-8637A6E1A080.jpeg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;550x291&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Keith’s Comic Books&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Free comic!&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;https://www.facebook.com/KeithscomicsOH/&quot;
                  },
                  &quot;imageId&quot;: &quot;611d910cba14021c54df4529&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;611d910cba14021c54df4529&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629327628040,
                    &quot;updatedOn&quot;: 1629327633335,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629327628040,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629327628774-SNXCD6J12GOV39KMTAP5&quot;,
                    &quot;systemDataVariants&quot;: &quot;2151x1252,100w,300w,500w,750w,1000w,1500w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;3A86FB91-D57B-42E3-B744-1D46A9F03B97.jpeg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;bab196&quot;,
                      &quot;topRightAverage&quot;: &quot;d4d1bb&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;050509&quot;,
                      &quot;bottomRightAverage&quot;: &quot;010201&quot;,
                      &quot;centerAverage&quot;: &quot;657a99&quot;,
                      &quot;suggestedBgColor&quot;: &quot;e8dca5&quot;
                    },
                    &quot;urlId&quot;: &quot;k3sq2jk4lci7eyiumoclxb0fqx8git&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629327628774-SNXCD6J12GOV39KMTAP5/3A86FB91-D57B-42E3-B744-1D46A9F03B97.jpeg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;2151x1252&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Gold Star Awards&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;10% discount for new clients on your first order with us on any trophy/plaque/name tag/engraved plate&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Expires 12/31/2021&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;http://goldstarawards.company&quot;
                  },
                  &quot;imageId&quot;: &quot;6124f9c5b437e10913e70778&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;6124f9c5b437e10913e70778&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629813189784,
                    &quot;updatedOn&quot;: 1629813192845,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629813189784,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629813190184-IB2ZIE9ZU0JI9TON98M2&quot;,
                    &quot;systemDataVariants&quot;: &quot;538x272,100w,300w,500w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;IMG_4326.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;topRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;centerAverage&quot;: &quot;9c8c6a&quot;,
                      &quot;suggestedBgColor&quot;: &quot;ffffff&quot;
                    },
                    &quot;urlId&quot;: &quot;zytprcelkvzbufjbc76ozwy2ao17ak&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629813190184-IB2ZIE9ZU0JI9TON98M2/IMG_4326.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;538x272&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Auto Details&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Receive 10% off on any complete detail package or window tint service with this offer.&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;Expires 12/31/2021&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit Website&quot;,
                    &quot;buttonLink&quot;: &quot;http://autodetails-elyria.com&quot;
                  },
                  &quot;imageId&quot;: &quot;612667121e05e462da4d549c&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;612667121e05e462da4d549c&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1629906706765,
                    &quot;updatedOn&quot;: 1629906709641,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1629906706765,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1629906706791-OH1V4ODL6OTOJDR43C1A&quot;,
                    &quot;systemDataVariants&quot;: &quot;754x754,100w,300w,500w,750w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;7f6c1508-1ddc-44cb-b1a4-c32f1c5acd4b-upload_your_logo-New-Logo.jpg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;topRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;ffffff&quot;,
                      &quot;bottomRightAverage&quot;: &quot;ffffff&quot;,
                      &quot;centerAverage&quot;: &quot;747474&quot;,
                      &quot;suggestedBgColor&quot;: &quot;ffffff&quot;
                    },
                    &quot;urlId&quot;: &quot;db1yowvbwwneh7d2s1x65z6kgrneuo&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1629906706791-OH1V4ODL6OTOJDR43C1A/7f6c1508-1ddc-44cb-b1a4-c32f1c5acd4b-upload_your_logo-New-Logo.jpg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;754x754&quot;
                  }
                }, {
                  &quot;title&quot;: &quot;Pearl’s Girls Knit and Stitch&quot;,
                  &quot;description&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;1/2 Price on “Big Box Store Yarn”&lt;\/p&gt;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;from 11 Oct till 29 Oct 2021&lt;\/p&gt;&quot;,
                  &quot;button&quot;: {
                    &quot;buttonText&quot;: &quot;Visit website&quot;,
                    &quot;buttonLink&quot;: &quot;https://pearls-girls-knit-stitch.business.site&quot;
                  },
                  &quot;imageId&quot;: &quot;61636cb3e182b11f3f199a1a&quot;,
                  &quot;mediaFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;image&quot;: {
                    &quot;id&quot;: &quot;61636cb3e182b11f3f199a1a&quot;,
                    &quot;recordType&quot;: 2,
                    &quot;addedOn&quot;: 1633905843733,
                    &quot;updatedOn&quot;: 1633905847610,
                    &quot;workflowState&quot;: 1,
                    &quot;publishOn&quot;: 1633905843733,
                    &quot;authorId&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                    &quot;systemDataId&quot;: &quot;1633905844185-H20DTN99TVJWD2L7AOTI&quot;,
                    &quot;systemDataVariants&quot;: &quot;1080x608,100w,300w,500w,750w,1000w&quot;,
                    &quot;systemDataSourceType&quot;: &quot;JPG&quot;,
                    &quot;filename&quot;: &quot;63A20093-029B-497C-AECD-5604A0F892F0.jpeg&quot;,
                    &quot;mediaFocalPoint&quot;: {
                      &quot;x&quot;: 0.5,
                      &quot;y&quot;: 0.5,
                      &quot;source&quot;: 3
                    },
                    &quot;colorData&quot;: {
                      &quot;topLeftAverage&quot;: &quot;2f402f&quot;,
                      &quot;topRightAverage&quot;: &quot;1c0f0d&quot;,
                      &quot;bottomLeftAverage&quot;: &quot;424661&quot;,
                      &quot;bottomRightAverage&quot;: &quot;060403&quot;,
                      &quot;centerAverage&quot;: &quot;1a1c1d&quot;,
                      &quot;suggestedBgColor&quot;: &quot;47634c&quot;
                    },
                    &quot;urlId&quot;: &quot;m8jrcs62dsp134w0ckxbl7zua97r9r&quot;,
                    &quot;title&quot;: &quot;&quot;,
                    &quot;body&quot;: null,
                    &quot;likeCount&quot;: 0,
                    &quot;commentCount&quot;: 0,
                    &quot;publicCommentCount&quot;: 0,
                    &quot;commentState&quot;: 2,
                    &quot;unsaved&quot;: false,
                    &quot;author&quot;: {
                      &quot;id&quot;: &quot;59ef3b8a5e0ed8f6df1daff0&quot;,
                      &quot;displayName&quot;: &quot;Irene Ng&quot;,
                      &quot;firstName&quot;: &quot;Irene&quot;,
                      &quot;lastName&quot;: &quot;Ng&quot;
                    },
                    &quot;assetUrl&quot;: &quot;https://images.squarespace-cdn.com/content/v1/60df22e8a2850757bb143aa1/1633905844185-H20DTN99TVJWD2L7AOTI/63A20093-029B-497C-AECD-5604A0F892F0.jpeg&quot;,
                    &quot;contentType&quot;: &quot;image/jpeg&quot;,
                    &quot;items&quot;: [ ],
                    &quot;pushedServices&quot;: { },
                    &quot;pendingPushedServices&quot;: { },
                    &quot;recordTypeLabel&quot;: &quot;image&quot;,
                    &quot;originalSize&quot;: &quot;1080x608&quot;
                  }
                } ],
                &quot;styles&quot;: {
                  &quot;imageFocalPoint&quot;: {
                    &quot;x&quot;: 0.5,
                    &quot;y&quot;: 0.5
                  },
                  &quot;imageOverlayOpacity&quot;: 0.3,
                  &quot;backgroundColor&quot;: &quot;white&quot;,
                  &quot;sectionTheme&quot;: &quot;white&quot;,
                  &quot;imageEffect&quot;: &quot;none&quot;,
                  &quot;backgroundMode&quot;: &quot;image&quot;,
                  &quot;backgroundImage&quot;: null
                },
                &quot;video&quot;: {
                  &quot;filter&quot;: 1,
                  &quot;videoFallbackContentItem&quot;: null,
                  &quot;nativeVideoContentItem&quot;: null,
                  &quot;videoSourceProvider&quot;: &quot;none&quot;
                },
                &quot;backgroundImageFocalPoint&quot;: null,
                &quot;backgroundImageId&quot;: null,
                &quot;options&quot;: {
                  &quot;maxColumns&quot;: 4,
                  &quot;isCardEnabled&quot;: true,
                  &quot;isMediaEnabled&quot;: true,
                  &quot;isTitleEnabled&quot;: true,
                  &quot;isBodyEnabled&quot;: true,
                  &quot;isButtonEnabled&quot;: true,
                  &quot;mediaAspectRatio&quot;: &quot;3:2&quot;,
                  &quot;layoutWidth&quot;: &quot;inset&quot;,
                  &quot;mediaWidth&quot;: {
                    &quot;value&quot;: 75,
                    &quot;unit&quot;: &quot;%&quot;
                  },
                  &quot;mediaAlignment&quot;: &quot;center&quot;,
                  &quot;contentWidth&quot;: {
                    &quot;value&quot;: 100,
                    &quot;unit&quot;: &quot;%&quot;
                  },
                  &quot;titleAlignment&quot;: &quot;center&quot;,
                  &quot;bodyAlignment&quot;: &quot;center&quot;,
                  &quot;buttonAlignment&quot;: &quot;center&quot;,
                  &quot;titlePlacement&quot;: &quot;center&quot;,
                  &quot;bodyPlacement&quot;: &quot;center&quot;,
                  &quot;buttonPlacement&quot;: &quot;center&quot;,
                  &quot;cardVerticalAlignment&quot;: &quot;top&quot;,
                  &quot;contentOrder&quot;: &quot;media-first&quot;,
                  &quot;verticalPaddingTop&quot;: {
                    &quot;value&quot;: 10,
                    &quot;unit&quot;: &quot;vmax&quot;
                  },
                  &quot;verticalPaddingBottom&quot;: {
                    &quot;value&quot;: 10,
                    &quot;unit&quot;: &quot;vmax&quot;
                  },
                  &quot;spaceBetweenColumns&quot;: {
                    &quot;value&quot;: 60,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;spaceBetweenRows&quot;: {
                    &quot;value&quot;: 60,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;spaceBetweenContentAndMedia&quot;: {
                    &quot;value&quot;: 6,
                    &quot;unit&quot;: &quot;%&quot;
                  },
                  &quot;spaceBelowTitle&quot;: {
                    &quot;value&quot;: 6,
                    &quot;unit&quot;: &quot;%&quot;
                  },
                  &quot;spaceBelowBody&quot;: {
                    &quot;value&quot;: 6,
                    &quot;unit&quot;: &quot;%&quot;
                  },
                  &quot;cardPaddingTop&quot;: {
                    &quot;value&quot;: 20,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;cardPaddingRight&quot;: {
                    &quot;value&quot;: 20,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;cardPaddingBottom&quot;: {
                    &quot;value&quot;: 20,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;cardPaddingLeft&quot;: {
                    &quot;value&quot;: 20,
                    &quot;unit&quot;: &quot;px&quot;
                  },
                  &quot;titleFontSize&quot;: &quot;heading-2&quot;,
                  &quot;bodyFontSize&quot;: &quot;paragraph-2&quot;,
                  &quot;buttonFontSize&quot;: &quot;button-medium&quot;,
                  &quot;customOptions&quot;: {
                    &quot;customTitleFontSize&quot;: {
                      &quot;value&quot;: 1.2,
                      &quot;unit&quot;: &quot;rem&quot;
                    },
                    &quot;customBodyFontSize&quot;: {
                      &quot;value&quot;: 0.9,
                      &quot;unit&quot;: &quot;rem&quot;
                    },
                    &quot;customButtonFontSize&quot;: {
                      &quot;value&quot;: 0.8,
                      &quot;unit&quot;: &quot;rem&quot;
                    }
                  }
                },
                &quot;layout&quot;: &quot;simple&quot;,
                &quot;isSectionTitleEnabled&quot;: true,
                &quot;sectionTitle&quot;: &quot;&lt;p class=\&quot;\&quot; style=\&quot;white-space:pre-wrap;\&quot;&gt;&amp;nbsp;All Participating Merchants and the Perks offered for the &lt;a href=\&quot;/elyria/passes\&quot; target=\&quot;\&quot;&gt;Elyria Resident Data Pass&lt;\/a&gt;&lt;\/p&gt;&quot;,
                &quot;spaceBelowSectionTitle&quot;: {
                  &quot;value&quot;: 70,
                  &quot;unit&quot;: &quot;px&quot;
                },
                &quot;sectionTitleAlignment&quot;: &quot;center&quot;,
                &quot;isSectionButtonEnabled&quot;: false,
                &quot;sectionButton&quot;: {
                  &quot;buttonText&quot;: &quot;&quot;,
                  &quot;buttonLink&quot;: &quot;#&quot;,
                  &quot;buttonNewWindow&quot;: false
                },
                &quot;sectionButtonSize&quot;: &quot;medium&quot;,
                &quot;sectionButtonAlignment&quot;: &quot;center&quot;,
                &quot;spaceAboveSectionButton&quot;: {
                  &quot;value&quot;: 70,
                  &quot;unit&quot;: &quot;px&quot;
                }
              }"""

data = json.loads(html.unescape(raw_data))

user_items = data['userItems']

item = user_items[0]

merchant_id = 'e171c72c-6677-4814-9e4b-60c26a36c161'
for item in user_items:
    title = '"{}"'.format(item['title'])
    description = BeautifulSoup(item['description'], 'html.parser')
    descrpt = '"{}"'.format(description.text)
    perk_url = item['button']['buttonLink']
    logo_url = perk_image_url = item['image']['assetUrl']
    print("{},{},{},end_date,{},{},{}".format(merchant_id, title, descrpt, perk_url, logo_url, perk_image_url))