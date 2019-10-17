import vk
from functools import reduce

class vktools(object):
    def __init__(self, token, version='5.102', lang='ru'):
        self.session = vk.Session(access_token=token)
        self.api = vk.API(self.session)
        self.version = version
        self.lang = lang
    
    def Friends(self, ids):
        try:
            friends = [set(self.api.friends.get(user_id=userid, v=self.version)['items']) for userid in ids]
            return list(reduce(lambda x,y: x | y, friends))
        except vk.exceptions.VkAPIError:
            return []

    def AllFriends(self, target, ids=[]):
        friends = set(self.Friends([target]))
        queue = list(friends) + ids
        while queue:
            last = queue.pop()
            if last not in friends and target in self.Friends([last]):
                friends.add(last)
            for userid in self.MutualFriends([target, last]):
                if userid not in friends:
                    friends.add(userid)
                    queue.append(userid)
        return list(friends)
    
    def LimitedMutualFriends(self, ids):
        return list(reduce(lambda x,y: x & y, [set(self.Friends([userid])) for userid in ids]))

    def UnlimitedMutualFriends(self, ids):
        friends = {userid: self.Friends([userid]) for userid in ids}
        result = set()
        for key, value in friends.items():
            for friend in value:
                newfriends = set(self.Friends([friend]))
                newfriends.add(key)
                if set(ids).issubset(newfriends):
                    result.add(friend)
        return list(result)

    def MutualFriends(self, ids):
        return list(set(self.LimitedMutualFriends(ids)) | set(self.UnlimitedMutualFriends(ids)))

    def GroupFriends(self, ids, groups):
        friends = self.Friends(ids)
        result = set()
        for groupid in groups:
            try:
                res = [ans['member'] for ans in self.api.groups.isMember(user_ids=friends, group_id=groupid, v=self.version)]
                result |= set(i[0] for i in zip(friends, res) if i[1])
            except vk.exceptions.VkAPIError:
                continue
        return list(result)
    
    def GetInfo(self, ids):
        try:
            return [self.api.users.get(user_ids=userid, v=self.version, lang=self.lang) for userid in ids]
        except vk.exceptions.VkException:
            return []
    
    def GetName(self, ids):
        return [userinfo[0]['first_name'] + ' ' + userinfo[0]['last_name'] for userinfo in self.GetInfo(ids)]

    def GetLink(self, ids):
        return ['https://vk.com/id' + str(userid) for userid in self.GetUserId(ids)]

    def GetGroupId(self, groups):
        try:
            return [group['id'] for group in self.api.groups.getById(group_ids=groups, v=self.version)]
        except vk.exceptions.VkAPIError:
            return []

    def GetUserId(self, ids):
        return [userinfo[0]['id'] for userinfo in self.GetInfo(ids)]

